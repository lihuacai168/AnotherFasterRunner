import time

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response

from usermanager import models


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

        if current_time - update_time >= 20 * 60:
            raise exceptions.AuthenticationFailed({
                "code": "9997",
                "msg": "登陆超时，请重新登陆",
                "success": False
            })

        return obj.user, obj

    def authenticate_header(self, request):
        return 'Auth Failed'
