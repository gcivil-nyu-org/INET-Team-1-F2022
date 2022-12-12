from django.test import TestCase
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, ProfileEditForm, NewLocationForm, UserEditForm, PreferenceEditForm
from django.urls import reverse
from .forms import LoginForm
from .models import Profile
from . import views
import datetime
from django.utils import timezone
from datetime import date, timedelta



# Create your tests here.
class Test_is_user_auth(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")

    def test_user(self):
        self.client.login(username="test", password="test")
        assert self.user.is_authenticated

    def test_user_cant_see_signup_page(self):
        self.client.login(username="test", password="test")
        response = self.client.get("signup")
        assert response.status_code == 404

    def test_user_cant_see_login_page(self):
        self.client.login(username="test", password="test")
        response = self.client.get("login")
        assert response.status_code == 404

    def test_user_login(self): # Tests redirection after user login
        Profile.objects.create(user=self.user, date_of_birth=datetime.date(1996, 5, 28))
        self.client.login(username="test", password="test")
        response = self.client.get('/account/',follow=True)
        self.assertEquals(response.status_code, 200)


class TestRegister(TestCase):
    def test_register_page(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_register_process(self):
        response = self.client.post(
            reverse("register"),
            data={
                "username": "foo",
                "email": "bar@gmail.com",
                "password": "foobar123123ABC@",
                "password2": "foobar123123ABC@",
            },
        )

        self.assertEqual(response.status_code, 200)

class TestLogin(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="test-profile", password="test-profile")

    def test_login_page(self):
        url_path = '/account/login/'
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)

    def test_login_process(self):
        url_path = '/account/login/'
        response = self.client.post(
            url_path,
            data={
                "username": "test-profile",
                "password": "test-profile",
            },
        )
        self.assertEqual(response.status_code, 302)
    
    def test_login_process_success(self):
        url_path = '/account/login/'
        response = self.client.post(
            url_path,
            data={
                "username": "test-profile1",
                "password": "test-profile",
            },
        )
        self.assertEqual(response.status_code, 200)

class TestDashboard(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="test-profile", password="test-profile")
        Profile.objects.create(user=self.user1, date_of_birth=datetime.date(1996, 5, 28))

        self.user2 = User.objects.create_user(username="test-profile2", password="test-profile2")
        Profile.objects.create(user=self.user2, date_of_birth=datetime.date(1996, 6, 28))

    def test_dashboard_page(self):
        url_path = ''
        profile1 = Profile.objects.get(user=self.user1)
        profile2 = Profile.objects.get(user=self.user2)
        
        profile1.proposal_datetime_local = "December 01, 2022 - 15:48:02"
        profile2.matches.add(profile1.id)  
        profile1.matched_with.add(profile2.id)    
        response = self.client.get(url_path)

        time_now = timezone.now()
        end_date = time_now + datetime.timedelta(days=10)
        profile1.proposal_datetime_local = end_date
        profile2.matches.add(profile1.id)  
        profile1.matched_with.add(profile2.id) 
        response = self.client.get(url_path)

        profile2.matches.clear()   
        profile1.matched_with.clear()
        response = self.client.get(url_path)

        self.assertEqual(response.status_code, 200)

class TestViews(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="test-profile", password="test-profile")
        Profile.objects.create(user=self.user1, date_of_birth=datetime.date(1996, 5, 28))

    def test_main_page(self):
        url_path = '/account/'
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 302)
        # login as user1
        self.client.login(username="test-profile", password="test-profile")
        assert self.user1.is_authenticated
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 200)
        
    
    def test_pref_page(self):
        self.client.login(username="test-profile", password="test-profile")
        profile2 = Profile.objects.get(user=self.user1)
        pk2 = profile2.id
        path_to_view = '/account/preferences/' + str(pk2) + "/"
        response = self.client.get(path_to_view)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'profile/preferences.html')

    def test_edit_redirect(self):
        response = self.client.get(reverse("edit"))
        self.assertEqual(response.status_code, 302)

    def test_profile_list_redirect(self):
        response = self.client.get(reverse("profile_list"))
        self.assertEqual(response.status_code, 302)
    
    def test_profile_liked_me(self):
        self.client.login(username="test-profile", password="test-profile")
        profile2 = Profile.objects.get(user=self.user1)
        pk2 = profile2.id
        path_to_view = '/account/profile_liked_me/' + str(pk2) + "/"
        response = self.client.get(path_to_view)
        self.assertEqual(response.status_code,404)
        # self.assertTemplateUsed(response, 'profile/profile_liked_me.html')

    def test_load_locations(self):   
        url_path = 'ajax/load-locations/' + "?cusine_id=1&boro_id=4"
        response = self.client.get(url_path)
        self.assertEqual(response.status_code,404)

    def test_edit_pref(self):   
        response = self.client.get("account/edit_preferences/")
        self.assertEqual(response.status_code,404)

    def test_edit_page(self):   
        response = self.client.get("account/edit/")
        self.assertEqual(response.status_code,404)

    def test_filter_pref(self):   
        response = self.client.get("/account/filter_profile_list/")
        self.assertEqual(response.status_code,302)

class TestProfile(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="test-profile", password="test-profile")
        Profile.objects.create(user=self.user1, date_of_birth=datetime.date(1996, 5, 28))

        self.user2 = User.objects.create_user(username="test-profile2", password="test-profile2")
        Profile.objects.create(user=self.user2, date_of_birth=datetime.date(1996, 6, 28))

        self.user3 = User.objects.create_user(username="test-profile3", password="test-profile3")
        Profile.objects.create(user=self.user3, date_of_birth=datetime.date(1997, 6, 28))


    def testCalculateAge(self):
        profileObj = Profile.objects.get(date_of_birth=datetime.date(1996, 5, 28))
        self.assertEqual(profileObj.calc_age, 26)

    #Tests ability to view other user's profiles
    def testProfileLoad(self):
        self.client.login(username="test-profile", password="test-profile")
        profile2 = Profile.objects.get(user=self.user2)
        pk2 = profile2.id
        # print("Profile2 id: ",pk2)
        # print("User2 id: ",profile2.user_id)
        path_to_view = '/account/profile/' + str(pk2) + "/"
        # print("Path: ",path_to_view)
        response = self.client.get(path_to_view)
        self.assertEqual(response.status_code,404)
        #self.assertTemplateUsed(response, 'profile/profile.html')

    def testLike(self):
        self.client.login(username="test-profile", password="test-profile")
        assert self.user1.is_authenticated
        profile1 = Profile.objects.get(user=self.user1)
        profile2 = Profile.objects.get(user=self.user2)
        print(views.profile)
        pk2 = profile2.id
        # print("Profile2 id: ",pk2)
        # print("User2 id: ",profile2.user_id)
        url_path = '/account/profile/' + str(pk2) + "/"

        response = self.client.post(
            url_path,
            data = {
                "like" : "like",
            },
        )
        print("testLike")
       
        
        self.assertEquals(profile1.likes.all().first(), profile2)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('filter_profile_list'), 
                                    status_code=302, target_status_code=200,
                                     msg_prefix='', fetch_redirect_response=True)

    def testHideRiderect(self): 
        pass

    def testLikeRidirect(self):
        pass

    #Tests match functionality
    def testLikedBy(self):
        profile1 = Profile.objects.get(user=self.user1)
        profile2 = Profile.objects.get(user=self.user2)

        profile2.likes.add(profile1.id)
        print("User2 likes: ",profile2.likes.all())
        print("User1 is liked by: ",profile1.liked_by.all().first())

        self.assertEquals(profile1.liked_by.all().first(), profile2)

    #Tests basic match functionality
    def testMatch(self):

        profile1 = Profile.objects.get(user=self.user1)
        profile2 = Profile.objects.get(user=self.user2)
        profile3 = Profile.objects.get(user=self.user3)

        profile2.likes.add(profile1.id)
        profile3.likes.add(profile1.id)
        profile3.likes.add(profile2.id)


        # login as user1
        self.client.login(username="test-profile", password="test-profile")
        assert self.user1.is_authenticated

        pk2 = profile2.id
        url_path = '/account/profile/' + str(pk2) + "/"
        response = self.client.post(
            url_path,
            data = {
                "match" : "match",
            },
        )

        #Check if liked and liked_by fields are cleared
        self.assertEquals(profile1.matches.all().first(), profile2)
        self.assertEquals(profile2.matched_with.all().first(), profile1)
        self.assertEqual(len(profile1.liked_by.all()), 0)
        self.assertEqual(len(profile1.likes.all()), 0)
        self.assertEqual(len(profile2.likes.all()), 0)
        self.assertEqual(len(profile3.likes.all()), 0)

        #TODO: Test redirection to dashboard
        # self.assertRedirects(response, reverse('filter_profile_list'), 
        #                             status_code=302, target_status_code=200,
        #                              msg_prefix='', fetch_redirect_response=True)



    def testHide(self):
        profile1 = Profile.objects.get(user=self.user1)
        profile2 = Profile.objects.get(user=self.user2)
        profile2.likes.add(profile1.id)

        # login as user1
        self.client.login(username="test-profile", password="test-profile")
        assert self.user1.is_authenticated

        pk2 = profile2.id
        url_path = '/account/profile/' + str(pk2) + "/"
        response = self.client.post(
            url_path,
            data = {
                "like" : "hide",
            },
        )

        self.assertEquals(profile1.hides.all().first(), profile2)
        self.assertEquals(profile2.hidden_by.all().first(), profile1)

    def testDecline(self):
        profile1 = Profile.objects.get(user=self.user1)
        profile2 = Profile.objects.get(user=self.user2)
        profile2.likes.add(profile1.id)

        # login as user1
        self.client.login(username="test-profile", password="test-profile")
        assert self.user1.is_authenticated

        pk2 = profile2.id
        url_path = '/account/profile/' + str(pk2) + "/"
        response = self.client.post(
            url_path,
            data = {
                "match" : "decline",
            },
        )

        self.assertEquals(profile1.declines.all().first(), profile2)
        self.assertEquals(profile2.declined_by.all().first(), profile1)



class TestFeedback(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="test-profile", password="test-profile")
        Profile.objects.create(user=self.user1, 
                                date_of_birth=datetime.date(1996, 5, 28),
                                proposal_datetime_local = timezone.now(),
                                location_dropdown ="Test Location" )

        self.user2 = User.objects.create_user(username="test-profile2", password="test-profile2")
        Profile.objects.create(user=self.user2, 
                            date_of_birth=datetime.date(1996, 6, 28),
                            )
    
    def formAvailable(self):
        print("-------Feedback: Testing Dashboard--------")
        profile1 = Profile.objects.get(user=self.user1)
        profile2 = Profile.objects.get(user=self.user2)

        profile1.matches.add(profile2)

        self.client.login(username="test-profile", password="test-profile")

        #Go to feedback form
        url_path = 'match_feedback'
        response = self.client.get(url_path)
        self.assertEqual(response.status_code, 302)





        



class TestForms(TestCase):
    def test_form_save(self):

        form = UserEditForm()
        form.cleaned_data = {}
        form.cleaned_data["first_name"] = "test_first_name"
        form.cleaned_data["last_name"] = "test_last_name"
        form.cleaned_data["email"] = "test_email"

        user = form.save()
        email = form.cleaned_data["email"]
        print(f"Email is  : {email}")
        assert email != user.email

    def test_meta(self):
        form = UserEditForm()
        meta = form.Meta()
        assert meta.model == User
        assert meta.fields == ("first_name", "last_name", "email")

    def test_profile_form_save(self):

        form = ProfileEditForm()
        form.cleaned_data = {}
        form.cleaned_data["about_me"] = "Hi!Im new"
        form.cleaned_data["occupation"] = "dentist"

        user_profile = form.save(False)
        occu = form.cleaned_data["occupation"]
        assert occu != user_profile.occupation
    
    def test_meta_profile(self):
        form = ProfileEditForm()
        meta = form.Meta()
        assert meta.model == Profile
        assert meta.fields not in ("about_me", "occupation")

    def test_location_form_save(self):
        form = NewLocationForm()
        form.cleaned_data = {}
        form.cleaned_data["cusine"] = "Mexican"
        form.cleaned_data["boro"] = "Manhattan"

        user_profile = form.save(False)
        cuisine = form.cleaned_data["cusine"]
        assert cuisine != user_profile.cusine
    
    def test_meta_location(self):
        form = NewLocationForm()
        meta = form.Meta()
        assert meta.model == Profile
        assert meta.fields == ("cusine", "boro", "location_dropdown")

    def test_pref_edit_form(self):
        form = PreferenceEditForm()
        # Set min age > max age to return false
        form.cleaned_data = {}
        form.cleaned_data["age_preference_min"] = 25
        form.cleaned_data["age_preference_max"] = 20
        self.assertEqual(False, form.check_age())
        # Set min age < max age to return True
        form.cleaned_data["age_preference_min"] = 25
        form.cleaned_data["age_preference_max"] = 30
        self.assertEqual(True, form.check_age())
