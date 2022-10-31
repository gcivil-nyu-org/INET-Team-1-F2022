from django.test import TestCase

# Create your tests here.
class Test_is_user_auth(TestCase):
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
    
    def test_reset_endpoint_returns_reset_page(client):
        response = client.get(path="account/")
        assert response.status_code == 200