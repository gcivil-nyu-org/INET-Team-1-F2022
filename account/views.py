import datetime
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, PreferenceEditForm, MatchFeedbackForm, TimeEditForm, NewLocationForm, UserEditForm, ProfileEditForm
from .models import Profile, newLocation

from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.db.models import Q

from django.core.paginator import Paginator  # for pagination of list views
from django.utils import timezone

from datetime import date, timedelta


def register(request):
    if request.user.is_authenticated:
        return redirect('/account')

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Get the age of user
            if not user_form.is_adult():
                return HttpResponse('Go home kid')
            dob = user_form.cleaned_data['date_of_birth']
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user, date_of_birth=dob)
            return render(request,
                          'account/registration_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/account')

    if request.method == 'POST':  # when user submits form via POST
        form = LoginForm(request.POST)  # instantiate form with submitted data
        if form.is_valid():
            # Authenticate user against database
            cd = form.cleaned_data
            # Returns the User object if authentication successful
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)  # set the user in session
                    return redirect('/account')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:  # when user_login view is called with a GET request
        form = LoginForm()  # instantiate a new login form
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    feedback_available = False
    user_profile = Profile.objects.get(user_id=request.user.id)
    time_now = timezone.now()
    # Check if the user is in a match and check if it has expired
    if user_profile.matches.all():
        # Get the other user profile who user_profile is matched with
        other_user_profile = user_profile.matches.first()
        # Check time against proposal time
        if user_profile.proposal_datetime_local != None:
            if time_now > user_profile.proposal_datetime_local + timedelta(hours=6):
                # Clear matches for both user_profile and the other profile
                user_profile.matches.clear()
                user_profile.feedback_submitted = False
                other_user_profile.matches.clear()
                other_user_profile.feedback_submitted = False
                msg = "Your match with " + other_user_profile.user.first_name + " has expired."
                messages.success(request, msg)
                user_profile.save()
                other_user_profile.save()
            else:
                print("There is still time left for your match/date!")
                if (time_now < user_profile.proposal_datetime_local + timedelta(hours=6) and
                    time_now > user_profile.proposal_datetime_local and
                        user_profile.feedback_submitted == False):
                    feedback_available = True
    elif user_profile.matched_with.all():
        print("I didn't match, but someone matched with me (matched_with)")
        other_user_profile = user_profile.matched_with.first()
        if time_now > other_user_profile.proposal_datetime_local + timedelta(hours=6):
            # Clear matches for both user_profile and the other profile
            user_profile.matches.clear()
            other_user_profile.matches.clear()
            user_profile.feedback_submitted = False
            other_user_profile.feedback_submitted = False
            msg = "Your match with " + other_user_profile.user.first_name + " has expired."
            messages.success(request, msg)
        else:
            # print("There is still time left for your match/date!")
            if (time_now < other_user_profile.proposal_datetime_local + timedelta(hours=6) and
                time_now > other_user_profile.proposal_datetime_local and
                    user_profile.feedback_submitted == False):
                feedback_available = True
    else:
        print("Not in a match at all")
        # Check if the user's time is now expired because proposal time < curr time
        if user_profile.proposal_datetime_local != None:
            if user_profile.proposal_datetime_local < time_now:
                msg = "Your proposal time " + str(user_profile.proposal_datetime_local) + " has now expired because it's in the past. Please update your time as soon as possible."
                messages.success(request, msg)

    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard', "user_profile": user_profile, "feedback_available": feedback_available})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)

        user_profile = request.user.profile
        user_id = request.user.id
        # print(user_id)
        if user_form.is_valid() and profile_form.is_valid():
            if user_form.check_username() == "":
                return render(request,
                              'account/edit.html',
                              {'user_form': user_form,
                               'profile_form': profile_form,
                               })
            # print(user_profile.proposal_datetime_local)
            user_form.save()
            profile_form.save()

            return redirect('profile', pk=user_id)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
        # location_form = NewLocationForm(instance=request.user.profile,
        #                             data=request.POST)

    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   })


@login_required
def edittimenplace(request):
    if request.method == 'POST':
        time_form = TimeEditForm(instance=request.user.profile,
                                 data=request.POST,
                                 files=request.FILES)

        user_profile = request.user.profile
        prev_time, prev_place = user_profile.proposal_datetime_local, user_profile.location_dropdown
        location_form = NewLocationForm(instance=request.user.profile,
                                        data=request.POST,
                                        files=request.FILES)

        user_id = request.user.id
        if time_form.is_valid() and location_form.is_valid():
            time_form.save()
            cur_time, cur_place = user_profile.proposal_datetime_local, user_profile.location_dropdown
            if cur_time != prev_time or cur_place != prev_place:
                user_profile.liked_by.clear()
            location_form.save()

            return redirect('profile', pk=user_id)
    else:
        prev_time, prev_place = request.user.profile.proposal_datetime_local, request.user.profile.location_dropdown
        time_form = TimeEditForm(instance=request.user.profile)
        location_form = NewLocationForm(instance=request.user.profile,
                                        data=request.POST)

    return render(request,
                  'account/edittimenplace.html',
                  {'time_form': time_form,
                   'location_form': location_form,
                   "prev_time": prev_time,
                   "prev_place": prev_place})


@login_required
def editplace(request):
    if request.method == 'POST':
        location_form = NewLocationForm(instance=request.user.profile,
                                        data=request.POST)
        # prev_place = request.user.profile.location_dropdown
        if location_form.is_valid():
            location_form.save()
            user_id = request.user.id
            return redirect('profile', pk=user_id)
    else:
        location_form = NewLocationForm(instance=request.user.profile,
                                        data=request.POST)
        # prev_place = request.user.profile.location_dropdown
    return render(request,
                  'account/edit_place.html',
                  {'location_form': location_form})


@login_required
def edittime(request):
    if request.method == 'POST':
        time_form = TimeEditForm(instance=request.user.profile,
                                 data=request.POST,
                                 files=request.FILES)
        user_id = request.user.id
        # Check if time is not valid
        if time_form.is_valid():
            if not time_form.check_time_is_valid():
                return render(request,
                  'account/edit_time.html',
                  {'time_form': time_form})
            if time_form.check_time_is_valid():
                prev_time = request.user.profile.proposal_datetime_local
                time_form.save()
                return redirect('profile', pk=user_id)
    else:
        time_form = TimeEditForm(instance=request.user.profile,
                                 data=request.POST,
                                 files=request.FILES)
        # prev_time = request.user.profile.proposal_datetime_local
    return render(request,
                  'account/edit_time.html',
                  {'time_form': time_form})


@login_required
def load_locations(request):
    cusine_id = request.GET.get('cusine_id')
    boro_id = request.GET.get('boro_id')
    locations = newLocation.objects.filter(CUISINE_id=cusine_id, BORO_id=boro_id)
    return render(request, 'profile/location_drop_down.html', {'locations': locations})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)


@login_required
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request,
                  'profile/profile_list.html',
                  {"profiles": profiles})


@login_required
def profile_liked_me(request, pk):
    if not get_referer(request):
        raise Http404
    # user = request.user.profile
    user_profile = Profile.objects.get(user_id=pk)

    # Check if current user's time has expired (is in past) then clear liked_me list
    time_now = timezone.now()
    if user_profile.proposal_datetime_local != None:
        if user_profile.proposal_datetime_local < time_now:
            # Clear liked_me list
            user_profile.liked_by.clear()
            msg = "Your proposal time has expired (is in the past). Because of this, all the likes you received have been cleared. Please update your proposal time ASAP."
            messages.success(request, msg)
    liked_me = user_profile.liked_by.all() # Pagination
    p = Paginator(liked_me, 5)
    page = request.GET.get('page')
    liked_me_list = p.get_page(page)
    return render(request,
                  'profile/profile_liked_me.html',
                  {"profile": user_profile,
                   "liked_me": liked_me_list})


@login_required
def profile(request, pk):
    if not get_referer(request) and request.method == "GET":
        raise Http404
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(user_id=pk)
    current_user_profile = request.user.profile
    if request.method == "POST":
        data = request.POST
        action_for_like_hide = data.get("like")
        action_for_match_decline = data.get("match")
        if action_for_like_hide == "like":
            current_user_profile.likes.add(profile.id)
            msg = "You have just liked " + profile.user.first_name + \
                ". We'll let you know if they decide to match with you."
            messages.success(request, msg)
            return redirect('filter_profile_list')
        elif action_for_like_hide == "hide":
            current_user_profile.hides.add(profile.id)
            msg = "You have just hidden " + profile.user.first_name + \
                ". Their proposals will no longer appear in this list."
            messages.success(request, msg)
            return redirect('filter_profile_list')
        elif action_for_match_decline == "match":
            current_user_profile.likes.clear() # Clear likes to ensure the users no longer appear in any 'Liked Me' list
            current_user_profile.liked_by.clear()
            current_user_profile.matches.add(profile.id)
            profile.likes.clear()
            profile.liked_by.clear()
            return redirect('dashboard')
        elif action_for_match_decline == "decline":
            # Add profile id to declined list
            current_user_profile.declines.add(profile.id)
            msg = "You have just declined to match with " + profile.user.first_name + \
                ". They will no longer appear in this list.\n Note that they will still be able to like any of your future proposals."
            messages.success(request, msg)
            return redirect('profile_liked_me', request.user.id)

        current_user_profile.save()
    return render(request,
                  "profile/profile.html",
                  {"profile": profile, "current_user_profile": current_user_profile})


@login_required
def preferences(request, pk):
    profile = Profile.objects.get(user_id=pk)

    return render(request,
                  "profile/preferences.html",
                  {"profile": profile})


@login_required
def edit_preferences(request):
    if request.method == 'POST':
        preference_form = PreferenceEditForm(
            instance=request.user.profile,
            data=request.POST)
        user_id = request.user.id
        if preference_form.is_valid():
            if not preference_form.check_age():
                return render(request,
                              'profile/edit_preferences.html',
                              {'preference_form': preference_form})
            if preference_form.check_age():
                preference_form.save()
                return redirect('profile', pk=user_id)
    else:
        preference_form = PreferenceEditForm(
            instance=request.user.profile)
    return render(request,
                  'profile/edit_preferences.html',
                  {'preference_form': preference_form})


@login_required
def filter_profile_list(request):
    gender_p = request.user.profile.gender_preference

    user_ids_to_exclude_likes = [
        userX.user.id for userX in request.user.profile.likes.all()]
    user_ids_to_exclude_likes.append(request.user.id)
    user_ids_to_exclude_hides = [
        userX.user.id for userX in request.user.profile.hides.all()]
    user_ids_to_exclude_likes.extend(user_ids_to_exclude_hides)

    # Add filter/check if proposal time > current system time, only then include these profiles as well
    time_now = timezone.now()
    if (gender_p == "Both"):
        profiles = Profile.objects.exclude(user_id__in=user_ids_to_exclude_likes).filter(
            Q(gender_identity="Man") | Q(gender_identity="Woman"))
    else:
        profiles = Profile.objects.exclude(user_id__in=user_ids_to_exclude_likes).filter(
            gender_identity=gender_p)

    profilesWithValidTime = []
    for profile in profiles:
        if profile.proposal_datetime_local != None:
            if profile.proposal_datetime_local > time_now:
                profilesWithValidTime.append(profile)

    # Pagination
    p = Paginator(profilesWithValidTime, 5)
    page = request.GET.get('page')
    profile_list = p.get_page(page)
    return render(request,
                  'profile/filter_profile_list.html',
                  {"profiles": profile_list, "currentuser": request.user.profile})


@login_required
def submitFeedback(request):
    if request.method == "POST":
        feedback_form = MatchFeedbackForm(
            data=request.POST)
        if feedback_form.is_valid():
            obj = feedback_form.save(commit=False)
            obj.feedback_user = User.objects.get(pk=request.user.id)
            if request.user.profile.matches.all():
                obj.matched_user = request.user.profile.matches.first().user
                obj.match_date = request.user.profile.proposal_datetime_local
                obj.match_location = request.user.profile.location_dropdown
            elif request.user.profile.matched_with.all():
                obj.matched_user = request.user.profile.matched_with.first().user
                obj.match_date = request.user.profile.matched_with.first().proposal_datetime_local
                obj.match_location = request.user.profile.matched_with.first().location_dropdown
            # if the user rated the matched user less than 5 , increment the warning of matched user
            if (int(feedback_form.cleaned_data.get('match_rating')) < 2) or (feedback_form.cleaned_data.get('inappropriate_behavior')) != None:
                obj.matched_user = request.user.profile.matches.first().user 
                obj.matched_user.profile.warning_count += 1
                print(obj.matched_user.profile.warning_count)
                obj.matched_user.profile.save()

            print("Feedback User:", obj.feedback_user)
            print("Match Comments: ", obj.match_comments)
            obj.save()

            request.user.profile.feedback_submitted = True
            request.user.profile.save()
            return redirect("dashboard")
        else:
            print(feedback_form.errors)
    else:
        feedback_form = MatchFeedbackForm(
            instance=request.user.profile)

        return render(request,
                      'account/match_feedback.html',
                      {'feedback_form': feedback_form,
                       'current_user_profile': request.user.profile}
                      )


def get_referer(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return None
    return referer


@login_required
def delete_account(request):
    # Get user object
    curr_user = User.objects.get(pk=request.user.id)
    curr_user.delete()
    # redirect to home
    # return render(request=request, template_name="main/home.html")
    return redirect("logout")


@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)

        # added error if old and new passwords are the same
        if request.POST.get("old_password", '0') == request.POST.get("new_password1", '0'):
            form.errors['same_pass'] = "Passwords can't be the same as the old one"
            return HttpResponse("Passwords can't be the same as the old one")

        # print(list(form.errors.values()))
        if form.is_valid() and len(form.errors.values()) == 0:
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = PasswordChangeForm(user)
    return render(request, 'registration/password_change_form.html', {'form': form})
