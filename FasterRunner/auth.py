import time

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from FasterRunner.settings.base import INVALID_TIME
from fastuser import models


def is_admin(token):
    is_permission = models.UserToken.objects.filter(token=token, user_id__level=1).first()
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
