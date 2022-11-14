from django.test import TestCase
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.urls import reverse
from .forms import LoginForm
from .models import Profile
import datetime


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
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'profile/profile.html')

    def testHide(self):
        pass

    def testLike(self):
        self.client.login(username="test-profile", password="test-profile")
        #profile1 = Profile.objects.get(user=self.user1)
        profile2 = Profile.objects.get(user=self.user2)

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
        self.assertEquals(response.status_code, 302)



    def testHideRiderect(self):
        pass

    def testLikeRidirect(self):
        pass


    