import time
import requests
from rest_framework import exceptions, response
from rest_framework.authentication import BaseAuthentication
from rest_framework.response import Response
from FasterRunner.settings import INVALID_TIME
from rest_framework import status
from usermanager import models


class Authenticator(BaseAuthentication):
    """
    账户鉴权认证 token
    """

    def authenticate(self, request):
        token = request.META.get("HTTP_TOKEN", None)
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