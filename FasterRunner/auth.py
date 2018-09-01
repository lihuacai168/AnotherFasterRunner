from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from usermanager import models


class Authenticator(BaseAuthentication):
    """
    账户鉴权认证 token
    """

    def authenticate(self, request):
        token = request.data.get("token", "none")
        obj = models.UserToken.objects.filter(token=token).first()

        if not obj:
            raise exceptions.AuthenticationFailed({
                "code": "9998",
                "msg": "用户未认证",
                "success": False
            })

        return (obj.user, obj)
