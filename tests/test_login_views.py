import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

# 使用实际的登录URL路径
login_url = "/api/user/login/"


@pytest.mark.django_db  # 如果你的测试需要数据库操作
class TestLoginView:
    def setup_method(self):
        User = get_user_model()
        User.objects.create_user('validUser', 'email@example.com', 'validPassword')

    def test_login_with_correct_credentials(self):
        client = APIClient()
        user_data = {"username": "validUser", "password": "validPassword"}
        response = client.post(login_url, user_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert (
            "token" in response.data
        )  # assuming that generate_token_and_respond returns a token in response

    def test_login_with_incorrect_credentials(self):
        client = APIClient()
        user_data = {"username": "invalidUser", "password": "invalidPassword"}
        response = client.post(login_url, user_data, format="json")
        # body
        assert response.json() == {'code': "0103", 'success': False, 'msg': "用户名或密码错误"}
        assert (
            response.status_code == status.HTTP_200_OK
        )  # assuming LOGIN_FAILED responds with status 401

    def test_login_with_no_credentials(self):
        client = APIClient()
        user_data = {}
        response = client.post(login_url, user_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_with_partial_credentials(self):
        client = APIClient()

        # Missing username
        user_data = {"password": "validPassword"}
        response = client.post(login_url, user_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # Missing password
        user_data = {"username": "validUser"}
        response = client.post(login_url, user_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
