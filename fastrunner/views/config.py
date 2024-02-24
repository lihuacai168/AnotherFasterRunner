from copy import deepcopy

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from fastrunner import models, serializers
from fastrunner.utils import response
from fastrunner.utils.decorator import request_log
from fastrunner.utils.parser import Format


class ConfigView(GenericViewSet):
    # authentication_classes = [OnlyGetAuthenticator, ]
    serializer_class = serializers.ConfigSerializer
    queryset = models.Config.objects

    @method_decorator(request_log(level="DEBUG"))
    def list(self, request):
        project = request.query_params["project"]
        search = request.query_params["search"]

        queryset = self.get_queryset().filter(project__id=project).order_by("-update_time")

        if search != "":
            queryset = queryset.filter(name__contains=search)

        pagination_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pagination_queryset, many=True)

        return self.get_paginated_response(serializer.data)

    @method_decorator(request_log(level="DEBUG"))
    def all(self, request, **kwargs):
        """
        get all config
        """
        pk = kwargs["pk"]

        queryset = (
            self.get_queryset()
            .filter(project__id=pk)
            .order_by("-update_time")
            .values("id", "name", "is_default", "base_url")
        )

        return Response(queryset)

    @method_decorator(request_log(level="INFO"))
    def add(self, request):
        """
        add new config
        {
            name: str
            project: int
            body: dict
        }
        """

        config = Format(request.data, level="config")
        config.parse()

        try:
            config.project = models.Project.objects.get(id=config.project)
        except ObjectDoesNotExist:
            return Response(response.PROJECT_NOT_EXISTS)

        if models.Config.objects.filter(name=config.name, project=config.project).first():
            return Response(response.CONFIG_EXISTS)

        config_body = {
            "name": config.name,
            "base_url": config.base_url,
            "body": config.testcase,
            "project": config.project,
        }

        models.Config.objects.create(**config_body, creator=request.user.username)
        return Response(response.CONFIG_ADD_SUCCESS)

    @method_decorator(request_log(level="INFO"))
    def update(self, request, **kwargs):
        """
        pk: int
        {
            name: str,
            base_url: str,
            variables: []
            parameters: []
            request: []
            }
        }
        """
        pk = kwargs["pk"]

        try:
            config = models.Config.objects.get(id=pk)

        except ObjectDoesNotExist:
            return Response(response.CONFIG_NOT_EXISTS)

        format = Format(request.data, level="config")
        format.parse()

        if models.Config.objects.exclude(id=pk).filter(name=format.name).first():
            return Response(response.CONFIG_EXISTS)

        case_step = models.CaseStep.objects.filter(method="config", name=config.name)

        for case in case_step:
            case.name = format.name
            case.body = format.testcase
            case.save()

        config.name = format.name
        config.body = format.testcase
        config.base_url = format.base_url
        if format.is_default is True:
            models.Config.objects.filter(project=config.project_id, is_default=True).update(is_default=False)
        config.is_default = format.is_default
        config.updater = request.user.username
        config.save()

        return Response(response.CONFIG_UPDATE_SUCCESS)

    @method_decorator(request_log(level="INFO"))
    def copy(self, request, **kwargs):
        """
        pk: int
        {
            name: str
        }
        """
        pk = kwargs["pk"]
        try:
            config = models.Config.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(response.CONFIG_NOT_EXISTS)

        if models.Config.objects.filter(**request.data).first():
            return Response(response.CONFIG_EXISTS)

        config.id = None
        config.is_default = False
        body = eval(config.body)
        name = request.data["name"]

        body["name"] = name
        config.name = name
        config.body = body
        config.creator = request.user.username
        config.updater = request.user.username
        config.save()

        return Response(response.CONFIG_ADD_SUCCESS)

    @method_decorator(request_log(level="INFO"))
    def delete(self, request, **kwargs):
        """
        删除一个配置 pk
        删除多个
        [{
            id:int
        }]
        """

        try:
            if kwargs.get("pk"):  # 单个删除
                config_obj = models.Config.objects.get(id=kwargs["pk"])
                if models.CaseStep.objects.filter(method="config", name=config_obj.name).exists():
                    return Response(response.CONFIG_IS_USED)
                config_obj.delete()
            else:
                delete_item = 0
                for content in request.data:
                    config_obj = models.Config.objects.get(id=content["id"])
                    if models.CaseStep.objects.filter(method="config", name=config_obj.name).exists():
                        continue
                    else:
                        config_obj.delete()
                        delete_item += 1
                if delete_item == 0:
                    return Response(response.CONFIG_IS_USED)

        except ObjectDoesNotExist:
            return Response(response.CONFIG_NOT_EXISTS)

        return Response(response.API_DEL_SUCCESS)


class VariablesView(GenericViewSet):
    serializer_class = serializers.VariablesSerializer
    queryset = models.Variables.objects

    @method_decorator(request_log(level="DEBUG"))
    def list(self, request):
        project = request.query_params["project"]
        search = request.query_params["search"]

        queryset = self.get_queryset().filter(project__id=project).order_by("-update_time")

        if search != "":
            queryset = queryset.filter(
                Q(key__contains=search) | Q(value__contains=search) | Q(description__contains=search)
            )

        pagination_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pagination_queryset, many=True)

        return self.get_paginated_response(serializer.data)

    @method_decorator(request_log(level="INFO"))
    def add(self, request):
        """
        add new variables
        {
            key: str
            value: str
            project: int
        }
        """
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            try:
                project = models.Project.objects.get(id=request.data["project"])
            except ObjectDoesNotExist:
                return Response(response.PROJECT_NOT_EXISTS)

            if models.Variables.objects.filter(key=request.data["key"], project=project).first():
                return Response(response.VARIABLES_EXISTS)

            request.data["project"] = project

            models.Variables.objects.create(**request.data)
            return Response(response.CONFIG_ADD_SUCCESS)
        else:
            res = deepcopy(response.PROJECT_NOT_EXISTS)
            res["msg"] = ser.errors
            return Response(res)

    @method_decorator(request_log(level="INFO"))
    def update(self, request, **kwargs):
        """
        pk: int
        {
          key: str
          value:str
        }
        """

        project_id = kwargs["pk"]
        variable_id = request.data["id"]
        try:
            variables = models.Variables.objects.get(id=variable_id)

        except ObjectDoesNotExist:
            return Response(response.VARIABLES_NOT_EXISTS)

        if (
            models.Variables.objects.exclude(id=variable_id)
            .filter(project_id=project_id, key=request.data["key"])
            .first()
        ):
            return Response(response.VARIABLES_EXISTS)

        variables.key = request.data["key"]
        variables.value = request.data["value"]
        variables.description = request.data["description"]
        variables.save()

        return Response(response.VARIABLES_UPDATE_SUCCESS)

    @method_decorator(request_log(level="INFO"))
    def delete(self, request, **kwargs):
        """
        删除一个变量 pk
        删除多个
        [{
            id:int
        }]
        """

        try:
            if kwargs.get("pk"):  # 单个删除
                models.Variables.objects.get(id=kwargs["pk"]).delete()
            else:
                for content in request.data:
                    models.Variables.objects.get(id=content["id"]).delete()

        except ObjectDoesNotExist:
            return Response(response.VARIABLES_NOT_EXISTS)

        return Response(response.API_DEL_SUCCESS)


class HostIPView(GenericViewSet):
    serializer_class = serializers.HostIPSerializer
    queryset = models.HostIP.objects

    @method_decorator(request_log(level="DEBUG"))
    def list(self, request):
        project = request.query_params["project"]
        queryset = self.get_queryset().filter(project__id=project).order_by("-update_time")
        pagination_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pagination_queryset, many=True)

        return self.get_paginated_response(serializer.data)

    @method_decorator(request_log(level="INFO"))
    def add(self, request):
        """
        add new variables
        {
            name: str
            value: str
            project: int
        }
        """

        try:
            project = models.Project.objects.get(id=request.data["project"])
        except ObjectDoesNotExist:
            return Response(response.PROJECT_NOT_EXISTS)

        if models.HostIP.objects.filter(name=request.data["name"], project=project).first():
            return Response(response.HOSTIP_EXISTS)

        request.data["project"] = project

        models.HostIP.objects.create(**request.data)
        return Response(response.HOSTIP_ADD_SUCCESS)

    @method_decorator(request_log(level="INFO"))
    def update(self, request, **kwargs):
        """pk: int{
          name: str
          value:str
        }
        """
        pk = kwargs["pk"]

        try:
            host = models.HostIP.objects.get(id=pk)

        except ObjectDoesNotExist:
            return Response(response.HOSTIP_NOT_EXISTS)

        if models.HostIP.objects.exclude(id=pk).filter(name=request.data["name"]).first():
            return Response(response.HOSTIP_EXISTS)

        host.name = request.data["name"]
        host.value = request.data["value"]
        host.save()

        return Response(response.HOSTIP_UPDATE_SUCCESS)

    @method_decorator(request_log(level="INFO"))
    def delete(self, request, **kwargs):
        """删除host"""
        try:
            models.HostIP.objects.get(id=kwargs["pk"]).delete()
        except ObjectDoesNotExist:
            return Response(response.HOSTIP_NOT_EXISTS)

        return Response(response.HOST_DEL_SUCCESS)

    @method_decorator(request_log(level="DEBUG"))
    def all(self, request, **kwargs):
        """
        get all config
        """
        pk = kwargs["pk"]

        queryset = self.get_queryset().filter(project__id=pk).order_by("-update_time").values("id", "name")

        return Response(queryset)
