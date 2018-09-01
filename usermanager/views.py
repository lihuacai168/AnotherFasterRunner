from rest_framework.response import Response
from rest_framework.views import APIView
from usermanager.utils import response
from usermanager import models
from usermanager import serializers
import logging
# Create your views here.
from usermanager.utils.token import generate_token
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger('FastRunner')


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

        if models.UserInfo.objects.filter(username=username).first():
            return Response(response.REGISTER_USERNAME_EXIST)

        if models.UserInfo.objects.filter(email=email).first():
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
        """
        try:
            username = request.data["username"]
            password = request.data["password"]
        except KeyError:
            return Response(response.KEY_MISS)

        obj = models.UserInfo.objects.filter(username=username).first()

        if not obj:
            return Response(response.LOGIN_FAILED)

        if not check_password(password, obj.password):
            return Response(response.LOGIN_FAILED)

        token = generate_token(username)

        try:
            models.UserToken.objects.update_or_create(user=obj, defaults={"token": token})
        except :
            return Response(response.SYSTEM_ERROR)
        else:
            response.LOGIN_SUCCESS["token"] = token
            return Response(response.LOGIN_SUCCESS)


