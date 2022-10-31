from django.test import TestCase
from django.contrib.auth.models import User


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

class AppViewTests(TestCase):
    def test_home_endpoint_returns_welcome_page(client):
        response = client.get(path="/")
        assert response.status_code == 200

    def test_login_endpoint_returns_login_page(client):
        response = client.get(path="login/")
        assert response.status_code == 200

    def test_register_endpoint_returns_login_page(client):
        response = client.get(path="register/")
        assert response.status_code == 200

    def test_password_endpoint_returns_password_page(client):
        response = client.get(path="password-reset/")
        assert response.status_code == 200

    def test_reset_endpoint_returns_reset_page(client):
        response = client.get(path="password-reset/done")
        assert response.status_code == 200
    
    def test_account_endpoint_returns_reset_page(client):
        response = client.get(path="account/")
        assert response.status_code == 200


