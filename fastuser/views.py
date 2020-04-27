import logging


from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView


from fastuser.common import response
from fastuser import models
from fastuser import serializers

from fastuser.common.token import generate_token
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

logger = logging.getLogger('FastRunner')

# 获取用户模型
User = get_user_model()


class RegisterView(APIView):
    authentication_classes = ()
    permission_classes = ()

    """
    注册:{
        "user": "demo"
        "password": "1321"
        "email": "1@1.com"
    }
    """

    def post(self, request):

        try:
            username = request.data["username"]
            password = request.data["password"]
            email = request.data["email"]
        except KeyError:
            return Response(response.KEY_MISS)

        if models.User.objects.filter(username=username).first():
            return Response(response.REGISTER_USERNAME_EXIST)

        if models.User.objects.filter(email=email).first():
            return Response(response.REGISTER_EMAIL_EXIST)

        request.data["password"] = make_password(password)

        serializer = serializers.UserInfoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(response.REGISTER_SUCCESS)
        else:
            return Response(response.SYSTEM_ERROR)


class LoginView(APIView):
    """
    登陆视图，用户名与密码匹配返回token
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        """
        用户名密码一致返回token
        {
            username: str
            password: str
        }
        """
        try:
            username = request.data["username"]
            password = request.data["password"]
        except KeyError:
            return Response(response.KEY_MISS)

        user = User.objects.filter(username=username).first()

        if not user:
            return Response(response.USER_NOT_EXISTS)

        if not check_password(password, user.password):
            return Response(response.LOGIN_FAILED)

        # token = generate_token(username)

        # try:
        #     models.UserToken.objects.update_or_create(user=user, defaults={"token": token})
        # except ObjectDoesNotExist:
        #     return Response(response.SYSTEM_ERROR)
        # else:
        #     from rest_framework_jwt.settings import api_settings
        #
        #     jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        #     jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        #
        #     payload = jwt_payload_handler(user)
        #     token = jwt_encode_handler(payload)
        #     response.LOGIN_SUCCESS["token"] = token
        #     response.LOGIN_SUCCESS["user"] = username
        #     return Response(response.LOGIN_SUCCESS)
        #
        #

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        response.LOGIN_SUCCESS["token"] = token
        response.LOGIN_SUCCESS["user"] = username
        return Response(response.LOGIN_SUCCESS)
