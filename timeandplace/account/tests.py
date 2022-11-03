from django.test import TestCase
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from django.urls import reverse
from .forms import LoginForm


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