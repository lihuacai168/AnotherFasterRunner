import logging
from typing import Optional

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import check_password, make_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from fastuser import models, serializers
from fastuser.common import response
from fastuser.serializers import UserLoginSerializer

# 获取用户模型
User = get_user_model()

logger = logging.getLogger(__name__)


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


def ldap_auth(username: str, password: str) -> Optional[User]:
    ldap_user = authenticate(username=username, password=password)
    if ldap_user and ldap_user.backend == "django_auth_ldap.backend.LDAPBackend":
        logger.info(f"LDAP authentication successful for {username}")
        local_user: User = User.objects.filter(username=username).first()
        if local_user:
            local_user.password = make_password(password)
            local_user.save(update_fields=["password"])
            logger.info(f"ldap认证通过，更新本地用户密码: {username}")
        return local_user
    logger.info(f"LDAP authentication failed for {username}")
    return None


def local_auth(username: str, password: str) -> Optional[User]:
    local_user = User.objects.filter(username=username).first()
    if not local_user:
        logger.warning(f"Local user does not exist: {username}")
        return None
    if local_user.is_active == 0:
        logger.warning(f"Local user is blocked: {username}")
        return None
    if not check_password(password, local_user.password):
        logger.warning(f"Local authentication failed: {username}")
        return None
    return local_user


def generate_token_and_respond(local_user: User):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(local_user)
    token = jwt_encode_handler(payload)
    response.LOGIN_SUCCESS["token"] = token
    response.LOGIN_SUCCESS["user"] = local_user.username
    response.LOGIN_SUCCESS["is_superuser"] = local_user.is_superuser
    response.LOGIN_SUCCESS["show_hosts"] = local_user.show_hosts
    return Response(response.LOGIN_SUCCESS)


class LoginView(APIView):
    """
    登陆视图，用户名与密码匹配返回token
    """

    authentication_classes = ()
    permission_classes = ()

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            username: str = serializer.validated_data["username"]
            password: str = serializer.validated_data["password"]
            masked_password = f"{password[0]}{'*' * (len(password) - 2)}{password[-1]}"
            logger.info(f"Received login request for {username=}, password={masked_password}")

            local_user = None
            if settings.USE_LDAP:
                logger.info(f"Attempting LDAP authentication for {username=}")
                local_user = ldap_auth(username, password)

            if not local_user:
                logger.info(
                    f"LDAP authentication failed or not enabled, falling back to local authentication for {username=}"
                )
                local_user = local_auth(username, password)

            if local_user:
                logger.info(f"Authentication successful for {username=}")
                return generate_token_and_respond(local_user)
            else:
                logger.info(f"Authentication failed for {username=}")
                return Response(response.LOGIN_FAILED)
        else:
            return Response(serializer.errors, status=400)


class UserView(APIView):
    def get(self, request):
        users = User.objects.filter(is_active=1)
        ser = serializers.UserModelSerializer(instance=users, many=True)
        return Response(ser.data)
