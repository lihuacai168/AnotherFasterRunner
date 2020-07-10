import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from fastrunner import models, serializers
from rest_framework.response import Response
from fastrunner.utils import response
from fastrunner.utils.decorator import request_log
from fastrunner.utils.parser import Format, Parse
from django.db import DataError
from django.db.models import Q

from rest_framework.schemas import AutoSchema,SchemaGenerator
import coreapi


class APITemplateViewSchema(AutoSchema):
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ('get',):
            extra_fields = [
              coreapi.Field('node'),
              coreapi.Field('project'),
              coreapi.Field('search'),
              coreapi.Field('tag'),
              coreapi.Field('rigEnv'),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


class APITemplateView(GenericViewSet):
    """
    API操作视图
    """
    serializer_class = serializers.APISerializer
    queryset = models.API.objects
    schema = APITemplateViewSchema()

    @method_decorator(request_log(level='DEBUG'))
    def list(self, request):
        """
        API列表
        """
        ser = serializers.AssertSerializer(data=request.query_params)
        if ser.is_valid():
            node = ser.validated_data.get('node')
            project = ser.validated_data.get('project')
            search = ser.validated_data.get('search')
            tag = ser.validated_data.get('tag')
            rig_env = ser.validated_data.get('rigEnv')
            delete = ser.validated_data.get('delete')

            queryset = self.get_queryset().filter(project__id=project, delete=delete).order_by('-update_time')

            if search != '':
                queryset = queryset.filter(Q(name__contains=search) | Q(url__contains=search))

            if node != '':
                queryset = queryset.filter(relation=node)

            if tag != '':
                queryset = queryset.filter(tag=tag)

            if rig_env != '':
                queryset = queryset.filter(rig_env=rig_env)

            pagination_queryset = self.paginate_queryset(queryset)
            serializer = self.get_serializer(pagination_queryset, many=True)

            return self.get_paginated_response(serializer.data)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

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
            'relation': api.relation
        }

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
        pk = kwargs['pk']
        api = Format(request.data)
        api.parse()

        api_body = {
            'name': api.name,
            'body': api.testcase,
            'url': api.url,
            'method': api.method,
        }

        try:
            models.API.objects.filter(id=pk).update(**api_body)
        except ObjectDoesNotExist:
            return Response(response.API_NOT_FOUND)

        return Response(response.API_UPDATE_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def copy(self, request, **kwargs):
        """
        pk int: test id
        {
            name: api name
        }
        """
        pk = kwargs['pk']
        name = request.data['name']
        api = models.API.objects.get(id=pk)
        body = eval(api.body)
        body["name"] = name
        api.body = body
        api.id = None
        api.name = name
        api.save()
        return Response(response.API_ADD_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def delete(self, request, **kwargs):
        """
        删除一个接口 pk
        删除多个
        [{
            id:int
        }]
        """

        try:
            if kwargs.get('pk'):  # 单个删除
                # models.API.objects.get(id=kwargs['pk']).delete()
                models.API.objects.filter(id=kwargs['pk']).update(delete=1, update_time=datetime.datetime.now())
            else:
                for content in request.data:
                    # models.API.objects.get(id=content['id']).delete()
                    models.API.objects.filter(id=content['id']).update(delete=1)

        except ObjectDoesNotExist:
            return Response(response.API_NOT_FOUND)

        return Response(response.API_DEL_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def add_tag(self, request, **kwargs):
        """
        更新接口的tag,暂时默认为调试成功

        [{
            id:int
        }]
        """

        try:
            if kwargs.get('pk'):  # 单个删除

                models.API.objects.filter(id=kwargs['pk']).update(tag=request.data['tag'], update_time=datetime.datetime.now())

        except ObjectDoesNotExist:
            return Response(response.API_NOT_FOUND)

        return Response(response.API_UPDATE_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def single(self, request, **kwargs):
        """
        查询单个api，返回body信息
        """
        try:
            api = models.API.objects.get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            return Response(response.API_NOT_FOUND)

        parse = Parse(eval(api.body))
        parse.parse_http()

        resp = {
            'id': api.id,
            'body': parse.testcase,
            'success': True,
        }

        return Response(resp)
