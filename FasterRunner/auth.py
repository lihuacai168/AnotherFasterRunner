import time

import jwt
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication, jwt_get_username_from_payload
from rest_framework_jwt.settings import api_settings
from FasterRunner.settings.base import INVALID_TIME
from fastuser import models

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


def is_admin(token):
    is_permission = models.MyUser.objects.filter(is_superuser=1).first()
    if not is_permission:
        raise exceptions.PermissionDenied({
            "code": "9996",
            "msg": "权限不足,请联系管理员",
            "success": False
        })
    else:
        return True


class OnlyGetAuthenticator(BaseAuthentication):
    """
    非管理员,只允许GET调用方法,不能执行,不能修改DebugTalk
    """

    def authenticate(self, request):
        if request.method != 'GET':
            token = request.query_params.get("token", None)
            is_admin(token)

    def authenticate_header(self, request):
        return 'PermissionDenied'


class Authenticator(BaseAuthentication):
    """
    账户鉴权认证 token
    """

    def authenticate(self, request):

        token = request.query_params.get("token", None)
        obj = models.UserToken.objects.filter(token=token).first()

        if not obj:
            raise exceptions.AuthenticationFailed({
                "code": "9998",
                "msg": "用户未认证",
                "success": False
            })

        update_time = int(obj.update_time.timestamp())
        current_time = int(time.time())

        if current_time - update_time >= INVALID_TIME:
            raise exceptions.AuthenticationFailed({
                "code": "9997",
                "msg": "登陆超时，请重新登陆",
                "success": False
            })

        # valid update valid time
        obj.token = token
        obj.save()

        return obj.user, obj

    def authenticate_header(self, request):
        return 'Auth Failed'


class DeleteAuthenticator(BaseAuthentication):
    """
    删除方法权限判断
    """

    def authenticate(self, request):
        if request.method == 'DELETE':
            token = request.query_params.get("token", None)
            is_admin(token)

    def authenticate_header(self, request):
        return 'PermissionDenied'


class MyJWTAuthentication(JSONWebTokenAuthentication):

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise, returns `None`.
        """
        # jwt_value = request.query_params.get("token", None)
        jwt_value = request.META.get('HTTP_AUTHORIZATION', None)
        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignature:
            msg = '签名过期'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = '签名解析失败'
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()

        user = self.authenticate_credentials(payload)

        return user, jwt_value

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """
        User = get_user_model()
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = _('Invalid payload.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get_by_natural_key(username)
        except User.DoesNotExist:
            msg = '用户不存在'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = '用户已禁用'
            raise exceptions.AuthenticationFailed(msg)

        return user
