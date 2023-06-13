import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.http import HttpResponse, JsonResponse

from fastuser.common import response
from fastuser import models
from fastuser import serializers
from dwebsocket.decorators import accept_websocket
from fastuser.common.token import generate_token
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

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

    @swagger_auto_schema(request_body=serializers.UserLoginSerialzer)
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

        if user.is_active == 0:
            return Response(response.USER_BLOCKED)

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
        response.LOGIN_SUCCESS["is_superuser"] = user.is_superuser
        response.LOGIN_SUCCESS["show_hosts"] = user.show_hosts
        return Response(response.LOGIN_SUCCESS)


class UserView(APIView):

    def get(self, request):
        users = User.objects.filter(is_active=1)
        ser = serializers.UserModelSerializer(instance=users, many=True)
        return Response(ser.data)


clients = {}


@accept_websocket
def link(request):
    if request.is_websocket():
        message = request.COOKIES.get("UUID")
        if message and len(message) == 8:
            user_id = message
        else:
            user_id = str(uuid.uuid1())[:8]
        print("客户端链接成功：" + user_id)
        clients[user_id] = request.websocket
        clients[user_id].send('userId-' + user_id)
        result = request.websocket.wait()
    else:
        return HttpResponse('请使用socket访问！')


def send(request):
    if request.method == 'GET':
        data = request.GET.get('data')
        track_id = request.headers.get('X-Custom-TrackId')
        if track_id not in clients:
            return JsonResponse({"code": "0003", "success": False, "msg": "socket user not exits"})
        clients[track_id].send(data.encode('utf-8'))
        return JsonResponse({"code": "0000", "success": True, "msg": "message send success"})
    elif request.method == 'POST':
        track_id = request.headers.get('X-Custom-TrackId')
        # data_list = request.POST.get('data_list')
        data_tmp = str(request.body.decode())
        data_list = str(request.body, encoding='utf-8').split('&')[2].replace('data_list=', '')
        if track_id not in clients:
            return JsonResponse({"code": "0003", "success": False, "msg": "socket user not exits"})
        clients[track_id].send(data_list.encode('utf-8'))
        return JsonResponse({"code": "0000", "success": True, "msg": "message send success"})
