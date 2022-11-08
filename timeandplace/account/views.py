from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm,PreferenceEditForm
from .models import Profile

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                            'account/registration_done.html',
                            {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                    'account/register.html',
                    {'user_form': user_form})

def user_login(request):
    if request.method == 'POST': # when user submits form via POST
        form = LoginForm(request.POST) # instantiate form with submitted data
        if form.is_valid(): 

            # Authenticate user against database
            cd = form.cleaned_data 

            # Returns the User object if authentication successful
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user) # set the user in session
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')

    else: # when user_login view is called with a GET request
        form = LoginForm() # instantiate a new login form
    return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request,
                     'account/dashboard.html',
                     {'section': 'dashboard'})


from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)                                
        user_id = request.user.id
        print(user_id)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile',pk=user_id)
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile)
    return render(request,
                    'account/edit.html',
                    {'user_form': user_form,
                    'profile_form': profile_form})
import datetime
@login_required
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    #age = datetime.datetime.now().date() - profile.date_of_birth
    #age = age.days // 365
    return render(request, 
                'profile/profile_list.html',
                {"profiles" : profiles})

@login_required
def profile_liked_me(request, pk):
    # user = request.user.profile
    user_profile = Profile.objects.get(user_id = pk)
    return render(request,
                'profile/profile_liked_me.html',
                {"profile" : user_profile})
import datetime
@login_required
def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(user_id=pk)
    current_user_profile = request.user.profile
    if request.method == "POST":
        data = request.POST
        action = data.get("like")
        if action == "like":
            current_user_profile.likes.add(profile.id)
        elif action == "hide":
            current_user_profile.hides.add(profile.id)
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
            preference_form.save()
            return redirect('profile',pk=user_id)
    else:
        preference_form = PreferenceEditForm(
                                    instance=request.user.profile)
    return render(request,
                    'profile/edit_preferences.html',
                    {'preference_form': preference_form})
@login_required
def filter_profile_list(request):
    age_p_min = request.user.profile.age_preference_min
    age_p_max = request.user.profile.age_preference_max
    gender_p = request.user.profile.gender_preference
    oreo_p = request.user.profile.orientation_preference


    user_ids_to_exclude_likes = [userX.user.id for userX in request.user.profile.likes.all()]
    user_ids_to_exclude_likes.append(request.user.id)
    user_ids_to_exclude_hides = [userX.user.id for userX in request.user.profile.hides.all()]
    user_ids_to_exclude_likes.extend(user_ids_to_exclude_hides)
    
    # To-Do: Debug the issue with profile_id not matching user_id
    print(request.user.profile.likes.all())
    print(request.user.profile.hides.all())
    
    profiles = Profile.objects.exclude(user_id__in=user_ids_to_exclude_likes).filter(gender_identity = gender_p , sexual_orientation=oreo_p)
    return render(request, 
                'profile/filter_profile_list.html',
                {"profiles" : profiles, "currentuser" : request.user.profile})