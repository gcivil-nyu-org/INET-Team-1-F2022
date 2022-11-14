from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile


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
    def test_login_page(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_process(self):
        response = self.client.post(
            reverse("login"),
            data={
                "username": "foo",
                "password": "foobar123123ABC@"
            },
        )
        self.assertEqual(response.status_code, 200)

class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.profile = Profile(user_id = self.user.id)

    def test_home_logged_user_endpoint_returns_dashboard_page(self):
        self.client.login(username="test", password="test")
        response = self.client.get(path="/")
        assert response.status_code == 200
        self.assertTemplateUsed(response, "main/base.html")
    
    def test_edit_not_returns_edit_page(self):
        self.client.login(username="test", password="test")
        response = self.client.get(path="edit/")
        assert response.status_code == 404
    
    def test_profile_list_not_returns_filter_page(self):
        self.client.login(username="test", password="test")
        response = self.client.get(path="profile_list/")
        assert response.status_code == 404

    def test_edit_preferences_list_not_returns_filter_page(self):
        self.client.login(username="test", password="test")
        response = self.client.get(path="profile_list/")
        assert response.status_code == 404
    
    def test_edit_filter_list_not_returns_filter_page(self):
        self.client.login(username="test", password="test")
        response = self.client.get(path="filter_profile_list/")
        assert response.status_code == 404

    def test_edit_returns_edit_page(self):
        self.client.login(username="test", password="test")
        profile_record = Profile.objects.get(pk = self.profile.user_id)
        user_record = User.objects.get(pk = self.user.id)
        response = self.client.post(
            reverse("edit"),
            data={
                "user_form": user_record,
                "profile_form": profile_record
            },
        )
        self.assertEqual(response.status_code, 200)


class TestPreferences(TestCase):
    user = User.objects.create_user(username="test112345", password="test1")
    profile = Profile(user_id = user.id)

    def test_preferences(self):
        self.profile.age_preference_min = 22
        self.profile.age_preference_max = 32
        self.profile.gender_identity = 'Man'
        self.profile.sexual_orientation = 'Straight'
        self.profile.gender_preference = 'Woman'
        self.profile.orientation_preference = 'Straight'
        self.profile.save()

        record = Profile.objects.get(pk = self.profile.user_id)
        self.assertEqual(record,self.profile)

    def test_preferences_page(self):
        url = reverse('preferences', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)




