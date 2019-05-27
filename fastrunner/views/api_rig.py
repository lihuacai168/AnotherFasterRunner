# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: api_rig.py 
# @Time : 2019/5/25 9:25
# @Email: lihuacai168@gmail.com
# @Software: PyCharm

from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from rest_framework.viewsets import GenericViewSet
from fastrunner import models, serializers
from rest_framework.response import Response
from fastrunner.utils import response
from fastrunner.utils.decorator import request_log
from fastrunner.utils.parser import Format
from django.db import DataError
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from fastuser import models as user_model
from fastrunner.utils.relation import API_RELATION

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


class APIRigView(GenericViewSet):
    authentication_classes = [Authenticator,]
    serializer_class = serializers.APISerializer
    queryset = models.API.objects

    def list(self, request):
        """
        接口列表 {
            project: int,
            node: int
        }
        """

        node = request.query_params["node"]
        project = request.query_params["project"]
        search = request.query_params["search"]
        # queryset = self.get_queryset().filter(project__id=project).order_by('-update_time')
        queryset = self.get_queryset().filter(project__id=project, delete=None).order_by('-update_time')
        # queryset = self.get_queryset().filter(Q(project__id=project) and ~Q(delete=1)).order_by('-update_time')


        if search != '':
            queryset = queryset.filter(name__contains=search)

        if node != '':
            queryset = queryset.filter(relation=node)

        pagination_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pagination_queryset, many=True)

        return self.get_paginated_response(serializer.data)

    @method_decorator(request_log(level='INFO'))
    def add(self, request):
        """
        新增一个接口
        """

        api = Format(request.data)
        api.parse()

        api_body = {
            'name': api.name,
            'body': api.testcase,
            'url': api.url,
            'method': api.method,
            'project': models.Project.objects.get(id=api.project),
            # 'relation': api.relation,
            'rig_id': api.rig_id,
        }
        try:
            relation = API_RELATION[api.relation]
        except KeyError:
            relation = API_RELATION['default']
        api_body['relation'] = relation
        try:
            models.API.objects.create(**api_body)
        except DataError:
            return Response(response.DATA_TO_LONG)

        return Response(response.API_ADD_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def update(self, request, **kwargs):
        """
        更新接口
        """
        pk = kwargs['rig_id']
        api = Format(request.data)
        api.parse()

        api_body = {
            'name': api.name,
            'body': api.testcase,
            'url': api.url,
            'method': api.method,
        }

        try:
            models.API.objects.filter(rig_id=pk).update(**api_body)
        except ObjectDoesNotExist:
            return Response(response.API_NOT_FOUND)
        return Response(response.API_UPDATE_SUCCESS)

