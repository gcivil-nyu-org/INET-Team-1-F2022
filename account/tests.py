import json
from django.test import TestCase
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, ProfileEditForm, NewLocationForm, UserEditForm, PreferenceEditForm, TimeEditForm
from django.urls import reverse
from .forms import LoginForm
from .models import Profile
from . import views
import datetime
from django.utils import timezone
from datetime import date, timedelta
import requests
from django.http import HttpRequest, Http404
from django.test.client import RequestFactory
from django.core.handlers.wsgi import WSGIRequest
from .views import edittimenplace, profile,load_locations,dashboard,edit, register, editplace, edittime,profile_liked_me, \
preferences,profile_list, edit_preferences,filter_profile_list,get_referer,submitFeedback, delete_account,password_change



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
        Profile.objects.create(user=self.user1, date_of_birth=datetime.date(1996, 5, 28), proposal_datetime_local ='2025-12-31T20:23')

        self.user2 = User.objects.create_user(username="test-profile2", password="test-profile2")
        Profile.objects.create(user=self.user2, date_of_birth=datetime.date(1996, 6, 28),proposal_datetime_local ='2025-12-31T20:23')

    def test_dashboard_page(self):
        profile1 = Profile.objects.get(user=self.user1)
        profile2 = Profile.objects.get(user=self.user2)

        # check path
        url_path = '/account/'
        response = self.client.get(url_path)
        self.assertEquals(response.status_code, 302)

        # check path
        req = HttpRequest()
        req.method = "GET"
        req.user = self.user1
        response = dashboard(req)
        assert response.status_code == 200

        # first if condition
        profile1.proposal_datetime_local = ['2025-12-31T20:23']
        profile1.matches.add(profile2.id)   
        self.assertEquals(profile1.matches.all().first(), profile2)
        response = self.client.get(url_path)

        req = HttpRequest()
        req.method = "GET"
        req.user = self.user1
        response = dashboard(req)
        assert response.status_code == 200

        #  elif condition
        profile1.proposal_datetime_local = ['2025-12-31T20:23']
        profile1.matches.clear()
        self.assertEquals(profile1.matches.all().first(), None)
        profile1.matched_with.add(profile2.id)   
        self.assertEquals(profile1.matched_with.all().first(), profile2)
        response = self.client.get(url_path)

        req = HttpRequest()
        req.method = "GET"
        req.user = self.user1
        response = dashboard(req)
        assert response.status_code == 200

        #else 
        profile1.proposal_datetime_local = ['2025-12-31T20:23']
        profile1.matched_with.clear()
        profile1.matches.clear()
        self.assertEquals(profile1.matched_with.all().first(), None)
        self.assertEquals(profile1.matches.all().first(), None)
        response = self.client.get(url_path)

        req = HttpRequest()
        req.method = "GET"
        req.user = self.user1
        response = dashboard(req)
        assert response.status_code == 200

class TestViews(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="test-profile", password="test-profile")
        Profile.objects.create(user=self.user1, date_of_birth=datetime.date(1996, 5, 28))
    
    def register_get(self):
        req = HttpRequest()
        req.method = "GET"
        req.user = self.user1
        response = register(req)
        assert response.status_code == 200
    
    def register_post(self):
        req = HttpRequest()
        req.method = "POST"
        req.user = self.user1
        req.POST = {'username': ['testuser_test'], 'first_name': ['testuser_test'], 'email': ['testuser_test@gmail.com'], 'date_of_birth_month': ['1'], 'date_of_birth_day': ['1'], 'date_of_birth_year': ['1998'], 'password': ['abcd@123'], 'password2': ['abcd@123'], 'csrfmiddlewaretoken': ['sN2x4QTGgimFVsy2JP10CMh8YRXB5wiqjmxhOAE5zWRAjau7Ip5NM4F7wEVBTDwD']}
        response = register(req)
        assert response.status_code == 200

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

        req = HttpRequest()
        req.method = "GET"
        req.user = self.user1
        profile1 = Profile.objects.get(user=self.user1)
        pk1 = profile1.id
        response = preferences(req, pk1)
        assert response.status_code == 200

    def test_edit_pref_post(self):
        req = HttpRequest()
        req.method = "POST"
        req.user = self.user1
        req.POST = {'age_preference_min': ['19'], 'age_preference_max': ['31'], 'gender_preference': ['Man'], 'csrfmiddlewaretoken': ['ZhI9Y5cQqmdHqZ6tUqe6klE75KdBkwvjClhNQo1jexKqAlWufcdgKxnZ4QaRYGTZ']}
        response = edit_preferences(req)
        assert response.status_code == 200

    def test_edit_pref_get(self):
        req = HttpRequest()
        req.method = "GET"
        req.user = self.user1
        response = edit_preferences(req)
        assert response.status_code == 200
        
    def test_edit_redirect(self):
        response = self.client.get(reverse("edit"))
        self.assertEqual(response.status_code, 302)

    def test_edit_post(self):
        req = HttpRequest()
        req.method = "POST"
        req.user = self.user1
        req.POST= {'first_name': ['Immonica'], 'last_name': ['Geller'], 'email': ['drc351@nyu.edu'], 'occupation': ['Chef'], 'about_me': ["I needed a plan, a plan to get over my man. And what's the opposite of man? Jam."], 'gender_identity': ['Woman'], 'photo': [''], 'csrfmiddlewaretoken': ['jJDc4NH9a1IpoOR3XnznFAL6ajVq8Yqpai8WOxsytFdkMwN8WXDaPS95I6TqW5EC']}
        response = edit(req)
        assert response.status_code == 200

    def test_edit_get(self):
        req = HttpRequest()
        req.method = "GET"
        req.user = self.user1
        response = edit(req)
        assert response.status_code == 200

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

        req = HttpRequest()
        req.method = "GET"
        req.user = self.user1
        response = get_referer(req)
        assert response == None

        req = HttpRequest()
        req.method = "GET"
        req.user = self.user1
        profile1 = Profile.objects.get(user=self.user1)
        pk1 = profile1.id
        referer = req.META.get('HTTP_REFERER')
        req.META['HTTP_REFERER'] = 'http://127.0.0.1:8082/account/'
        # req.META['HTTP_REFERER'] = 'http://timeandplacenyu-dev.eba-is5hjkxj.us-east-1.elasticbeanstalk.com/account/'
        response = profile_liked_me(req, pk1)
        self.assertEqual(response.status_code, 200)

    def test_load_locations(self):   
        url_path = 'ajax/load-locations/' + "?cusine_id=1&boro_id=4"
        response = self.client.get(url_path)
        self.assertEqual(response.status_code,404)

        req = HttpRequest()
        req.method = "GET"
        req.user = self.user1
        req.GET = {'cusine_id': 2,
                   'boro_id': 4}
        response = load_locations(req)
        assert response.status_code == 200

    def test_edit_pref(self):   
        response = self.client.get("account/edit_preferences/")
        self.assertEqual(response.status_code,404)

    def test_edit_page(self):   
        response = self.client.get("account/edit/")
        self.assertEqual(response.status_code,404)

    def test_profile_list(self):
        response = self.client.get("/account/profile_list/")
        self.assertTemplateUsed('profile/profile_list.html')
        self.assertEqual(response.status_code,302)

    def test_filter_pref(self):   
        response = self.client.get("/account/filter_profile_list/")
        self.assertEqual(response.status_code,302)

        req = HttpRequest()
        req.method = "GET"
        req.user = self.user1

        # set preferences before filtering
        req.POST = {'age_preference_min': ['19'], 'age_preference_max': ['31'], 'gender_preference': ['Man'], 'csrfmiddlewaretoken': ['ZhI9Y5cQqmdHqZ6tUqe6klE75KdBkwvjClhNQo1jexKqAlWufcdgKxnZ4QaRYGTZ']}
        response = edit_preferences(req)

        response = filter_profile_list(req)
        assert response.status_code == 200
        
    def test_edit_time_get(self):   
        response = self.client.get("/account/edit_time/")
        self.assertEqual(response.status_code,302)
       
        req = HttpRequest()
        req.method = "GET"
        req.user = self.user1
        response = edittime(req)
        assert response.status_code == 200
    
    def test_edit_place_get(self):   
        response = self.client.get("/account/edit_place/")
        self.assertEqual(response.status_code,302)        

        req = HttpRequest()
        req.method = "GET"
        req.user = self.user1
        response = editplace(req)
        
        assert response.status_code == 200
    
    def test_edit_time_place_get(self):   
        response = self.client.get("/account/edit_timenplace/")
        self.assertEqual(response.status_code,302)

        req = HttpRequest()
        req.method = "GET"
        req.user = self.user1
        response = edittimenplace(req)
        assert response.status_code == 200
        

    def test_edit_time_post(self):
        time_form = TimeEditForm()
        time_form.cleaned_data = {}
        time_form.cleaned_data["proposal_datetime_local"] = ['2022-12-17T20:23']

        url_path = '/account/edit_time/'
        response = self.client.post(
            url_path,
            data = {'time_form': time_form},
        )
        self.assertEqual(response.status_code, 302)

        req = HttpRequest()
        req.method = "POST"
        req.POST = {'time_form': time_form}
        req.user = self.user1
        response = edittime(req)
        assert response.status_code == 200

        req.POST = {'proposal_datetime_local': ['2022-12-17T20:23'], 'csrfmiddlewaretoken': ['oeUyACL20WNyvOBNqCPZ5wdRjQmF4LmXVVuupA7XuA5mEhA3BWqvcAohYWmEJZg5']}
        response = edittime(req)
        assert response.status_code == 200
    
    def test_edit_place_post(self):
        location_form = NewLocationForm()
        location_form.cleaned_data = {}
        location_form.cleaned_data["cusine"] = ['2']
        location_form.cleaned_data["boro"] = ['2']
        location_form.cleaned_data["location_dropdown"] = ['957']

        url_path = '/account/edit_place/'
        response = self.client.post(
            url_path,
            data = {'location_form': location_form},
        )
        self.assertEqual(response.status_code, 302)

        req = HttpRequest()
        req.method = "POST"
        req.POST = {'cusine': ['2'], 'boro': ['2'], 'location_dropdown': ['957'], 'csrfmiddlewaretoken': ['oeUyACL20WNyvOBNqCPZ5wdRjQmF4LmXVVuupA7XuA5mEhA3BWqvcAohYWmEJZg5']}
        # req.send(json.stringify(parameters))
        req.user = self.user1
        response = editplace(req)
        
        assert response.status_code == 200
        
    def test_editplace_get(self):
        response = self.client.get("/account/editplace/")
        self.assertEqual(response.status_code,404)
        #response = editplace(req)
        print("EDIT PLACE", response.status_code)
        response = self.client.get("/account/edit_timenplace/")
        self.assertEqual(response.status_code,302)
        #assert response.status_code == 200
        self.assertTemplateNotUsed( 'account/edit_place.html')

    def test_edit_timenplace_post(self):
        location_form = NewLocationForm()
        location_form.cleaned_data = {}
        location_form.cleaned_data["cusine"] = ['2']
        location_form.cleaned_data["boro"] = ['2']
        location_form.cleaned_data["location_dropdown"] = ['957']

        time_form = TimeEditForm()
        time_form.cleaned_data = {}
        time_form.cleaned_data["proposal_datetime_local"] = ['2022-12-17T20:23']

        url_path = '/account/edit_timenplace/'
        response = self.client.post(
            url_path,
            data = {'time_form': time_form,
                   'location_form': location_form},
        )
        self.assertEqual(response.status_code, 302)

        req = HttpRequest()
        req.method = "POST"
        req.POST = {'time_form': time_form,
                   'location_form': location_form}
        req.user = self.user1
        response = edittimenplace(req)
        assert response.status_code == 200


        req = HttpRequest()
        req.method = "POST"
        req.POST = {'proposal_datetime_local': ['2022-12-17T20:23'], 'cusine': ['2'], 'boro': ['2'], 'location_dropdown': ['957'], 'csrfmiddlewaretoken': ['oeUyACL20WNyvOBNqCPZ5wdRjQmF4LmXVVuupA7XuA5mEhA3BWqvcAohYWmEJZg5']}
        # req.send(json.stringify(parameters))
        req.user = self.user1
        response = edittimenplace(req)
        assert response.status_code == 200 


    def test_password_change(self):
        #repeat password
        req = HttpRequest()
        req.method = 'POST'
        req.user = self.user1
        req.POST = {'old_password': ['test-profile'], 'new_password1': ['test-profile'], 'new_password2': ['test-profile'], 'csrfmiddlewaretoken': ['oeUyACL20WNyvOBNqCPZ5wdRjQmF4LmXVVuupA7XuA5mEhA3BWqvcAohYWmEJZg5']}
        response = password_change(req)
        self.assertEqual(response.content, "Passwords can't be the same as the old one")
        assert response.status_code == 200


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
        pk1 = profile1.id
        # print("Profile2 id: ",pk2)
        # print("User2 id: ",profile2.user_id)
        url_path = '/account/profile/' + str(pk2) + "/"

        response = self.client.post(
            url_path,
            data = {
                "like" : "like",
            },
        )
        req = HttpRequest()
        req.method = "POST"
        req.POST = {'like': ['like']}
        req.user = self.user1
        response = profile(req, pk1)
        assert response.status_code == 200   
       
        self.assertEquals(profile1.likes.all().first(), profile2)
        self.assertEquals(response.status_code, 200)
        # self.assertRedirects(response, reverse('filter_profile_list'), 
        #                             status_code=302, target_status_code=200,
        #                              msg_prefix='', fetch_redirect_response=True)

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
        self.assertFalse(profile1.liked_by.exists())
        self.assertFalse(profile1.likes.exists())
        self.assertFalse(profile2.likes.exists())
        self.assertFalse(profile3.likes.exists())

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
        self.assertEqual(response.status_code, 302)

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

        req = HttpRequest()
        req.method = "GET"
        req.user = self.user1
        response = submitFeedback(req)
        assert response.status_code == 200 

    def feedback_form_post(self):  
        req = HttpRequest()
        req.method = "POST"
        req.user = self.user1
        req.POST = {'date_happened': ['Yes'], 'match_rating': ['3'], 'inappropriate_behavior': ['Uncomfortable'], 'match_comments': ['not comfy'], 'csrfmiddlewaretoken': ['WBA9cswIxf9gqMyOoQAGHYpuptPkYoxl8Q0yrVwIplABb4SWFXvxgGf4GO7wafOO']}
        response = submitFeedback(req)
        assert response.status_code == 200
    
    def delete_account_get(self):  
        req = HttpRequest()
        req.method = "GET"
        req.user = self.user2
        response = delete_account(req)
        assert response.status_code == 200
    
    def password_change_post(self):  
        req = HttpRequest()
        req.method = "POST"
        req.user = self.user2
        req.POST = {'old_password': ['abcd@123'], 'new_password1': ['abcd@1234'], 'new_password2': ['abcd@1234'], 'csrfmiddlewaretoken': ['qLkcRcO6JCm2ba17kfXvhcXOxJrjIh8dVBkDNbqI6qRMPO1GsijovP9OyfRWhWjX']}
        response = password_change(req)
        assert response.status_code == 200

        # password too short , not 8 chars
        req = HttpRequest()
        req.method = "POST"
        req.user = self.user2
        req.POST = {'old_password': ['abcd@123'], 'new_password1': ['1'], 'new_password2': ['1'], 'csrfmiddlewaretoken': ['qLkcRcO6JCm2ba17kfXvhcXOxJrjIh8dVBkDNbqI6qRMPO1GsijovP9OyfRWhWjX']}
        response = password_change(req)
        self.assertEqual(response.content, "This password is too short. It must contain at least 8 characters. \
                                            This password is too common. \
                                            This password is entirely numeric.")
        assert response.status_code == 200
    

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

    def test_pref_edit_form_age_preference(self):
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
    
    def test_user_registration_form_dob(self):
        form = UserRegistrationForm()
        form.cleaned_data = {}
        # test out dob making someone an adult
        form.cleaned_data["date_of_birth"] = date(1988, 5, 26)
        self.assertEqual(True, form.is_adult())
        # test out dob making someone a minor (not an adult)
        form.cleaned_data["date_of_birth"] = date(2005, 5, 26)
        self.assertEqual(False, form.is_adult())

    def test_user_edit_username(self):
        form = UserEditForm()
        form.cleaned_data = {}
        # Make blank username and check if check_username catches blank username
        form.cleaned_data["first_name"] = ""
        self.assertEqual("", form.check_username())
        # This should raise a validation error
        #self.assertTrue('First Name cannot be empty!')

    def test_meta_time(self):
        form = TimeEditForm()
        meta = form.Meta()
        assert meta.model == Profile
        assert meta.fields != ("proposal_datetime_local")

    def test_edit_time_form(self):
        form = TimeEditForm()
        form.cleaned_data = {}
        form.cleaned_data["proposal_datetime_local"] = timezone.now()
        self.assertNotEqual(timezone.now(), form.cleaned_data["proposal_datetime_local"])