# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: api_rig.py 
# @Time : 2019/5/25 9:25
# @Email: lihuacai168@gmail.com
# @Software: PyCharm

from rest_framework.viewsets import GenericViewSet
from fastrunner import models, serializers

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework import pagination
from fastuser import models as user_model
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class Authenticator(BaseAuthentication):
    """
    账户鉴权认证 token
    """

    def authenticate(self, request):
        token = request.query_params.get("token", None)
        obj = user_model.UserToken.objects.filter(token=token).first()

        if not obj:
            raise exceptions.AuthenticationFailed({
                "code": "9999",
                "msg": "用户未认证",
                "success": False
            })
        # valid update valid time
        obj.token = token
        obj.save()

        return obj.user, obj

    def authenticate_header(self, request):
        return 'Auth Failed'


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 500
    page_size_query_param = 'page_size'
    max_page_size = 10000


class APIRigView(GenericViewSet):
    authentication_classes = [Authenticator, ]
    serializer_class = serializers.APISerializer
    pagination_class = LargeResultsSetPagination
    queryset = models.API.objects
    renderer_classes = [JSONRenderer]

    def list(self, request):
        """
        procject:项目id
        search:搜索api的name
        env:环境 0,测试 1,生产 空值代表全部
        """

        project = request.query_params["project"]
        search = request.query_params["search"]
        env = request.query_params["env"]
        queryset = self.get_queryset().filter(project__id=project, delete=0).order_by('-update_time')
        if env != '':
            queryset = queryset.filter(rig_env=env)
        if search != '':
            queryset = queryset.filter(name__contains=search)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

        # pagination_queryset = self.paginate_queryset(queryset)
        # serializer = self.get_serializer(pagination_queryset, many=True)
        # return self.get_paginated_response(serializer.data)
