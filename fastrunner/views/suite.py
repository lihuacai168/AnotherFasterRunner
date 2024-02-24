import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from fastrunner import models, serializers
from fastrunner.utils import prepare, response
from fastrunner.utils.decorator import request_log


class TestCaseView(GenericViewSet):
    queryset = models.Case.objects
    serializer_class = serializers.CaseSerializer
    tag_options = {
        "冒烟用例": 1,
        "集成用例": 2,
        "监控脚本": 3,
        "核心用例": 4,
    }

    @staticmethod
    def case_step_search(search):
        """
        搜索case_step的url或者name
        返回对应的case_id
        """
        case_id = models.CaseStep.objects.filter(Q(name__contains=search) | Q(url__contains=search)).values("case_id")

        case_id = set([item["case_id"] for _, item in enumerate(case_id)])
        return case_id

    @method_decorator(request_log(level="INFO"))
    def get(self, request):
        """
        查询指定CASE列表，不包含CASE STEP
        {
            "project": int,
            "node": int
        }
        """
        ser = serializers.CaseSearchSerializer(data=request.query_params)
        if ser.is_valid():
            node = ser.validated_data.get("node")
            project = ser.validated_data.get("project")
            search = ser.validated_data.get("search")
            search_type = ser.validated_data.get("searchType")
            case_type = ser.validated_data.get("caseType")
            only_me = ser.validated_data.get("onlyMe")

            # update_time 降序排列
            queryset = self.get_queryset().filter(project__id=project).order_by("-create_time")

            if only_me is True:
                queryset = queryset.filter(creator=request.user)

            if node != "":
                queryset = queryset.filter(relation=node)

            if case_type != "":
                queryset = queryset.filter(tag=case_type)

            if search != "":
                # 用例名称搜索
                if search_type == "1":
                    queryset = queryset.filter(name__contains=search)
                # API名称或者API URL搜索
                elif search_type == "2":
                    case_id = self.case_step_search(search)
                    queryset = queryset.filter(pk__in=case_id)

            pagination_query = self.paginate_queryset(queryset)
            serializer = self.get_serializer(pagination_query, many=True)

            return self.get_paginated_response(serializer.data)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(request_log(level="INFO"))
    def copy(self, request, **kwargs):
        """
        pk int: test id
        {
            name: test name
            relation: int
            project: int
        }
        """
        pk = kwargs["pk"]
        name = request.data["name"]
        username = request.user.username
        if "|" in name:
            resp = self.split(pk, name)
        else:
            case = models.Case.objects.get(id=pk)
            case.id = None
            case.name = name
            case.creator = username
            case.updater = username
            case.save()

            case_step = models.CaseStep.objects.filter(case__id=pk)

            for step in case_step:
                step.id = None
                step.case = case
                step.creator = username
                step.updater = username
                step.save()
            resp = response.CASE_ADD_SUCCESS

        return Response(resp)

    def split(self, pk, name):
        split_case_name = name.split("|")[0]
        split_condition = name.split("|")[1]

        # 更新原本的case长度
        case = models.Case.objects.get(id=pk)
        case_step = models.CaseStep.objects.filter(case__id=pk, name__icontains=split_condition)
        # case_step = case_step.filter(Q(method='config') | Q(name__icontains=split_condition))
        case_step_length = len(case_step)
        case.length -= case_step_length
        case.save()

        new_case = models.Case.objects.filter(name=split_case_name).last()
        if new_case:
            new_case.length += case_step_length
            new_case.save()
            case_step.update(case=new_case)
        else:
            # 创建一条新的case
            case.id = None
            case.name = split_case_name
            case.length = case_step_length
            case.save()

            # 把原来的case_step中的case_id改成新的case_id
            case_step.update(case=case)
        # case_step.filter(name=).update_or_create(defaults={'case_id': case.id})
        return response.CASE_SPILT_SUCCESS

    @method_decorator(request_log(level="INFO"))
    def patch(self, request, **kwargs):
        """
        更新测试用例集
        {
            name: str
            id: int
            body: []
            project: int
        }
        """

        pk = kwargs["pk"]
        project = request.data.pop("project")
        body = request.data.pop("body")
        relation = request.data.pop("relation")

        is_exist_case_obj = models.Case.objects.exclude(id=pk).filter(name=request.data["name"], project__id=project)
        if relation:
            # 兼容新建用例时，保存用例步骤就提交修改
            is_exist_case_obj = is_exist_case_obj.filter(relation=relation)
        if is_exist_case_obj.first():
            return Response(response.CASE_EXISTS)

        case = models.Case.objects.get(id=pk)

        prepare.update_casestep(body, case, username=request.user.username)

        request.data["tag"] = self.tag_options[request.data["tag"]]
        models.Case.objects.filter(id=pk).update(
            update_time=datetime.datetime.now(),
            updater=request.user.username,
            **request.data,
        )

        return Response(response.CASE_UPDATE_SUCCESS)

    @method_decorator(request_log(level="INFO"))
    def move(self, request):
        project: int = request.data.get("project")
        relation: int = request.data.get("relation")
        cases: list = request.data.get("case")
        ids = [case["id"] for case in cases]
        try:
            models.Case.objects.filter(project=project, id__in=ids).update(relation=relation)
        except ObjectDoesNotExist:
            return Response(response.CASE_NOT_EXISTS)

        return Response(response.CASE_UPDATE_SUCCESS)

    @method_decorator(request_log(level="INFO"))
    def post(self, request):
        """
        新增测试用例集
        {
            name: str
            project: int,
            relation: int,
            tag:str
            body: [{
                id: int,
                project: int,
                name: str,
                method: str,
                url: str,
                source_api_id: int
            }]
        }
        """

        try:
            pk = request.data["project"]
            request.data["project"] = models.Project.objects.get(id=pk)

        except KeyError:
            return Response(response.KEY_MISS)

        except ObjectDoesNotExist:
            return Response(response.PROJECT_NOT_EXISTS)

        body = request.data.pop("body")

        request.data["tag"] = self.tag_options[request.data["tag"]]
        with transaction.atomic():
            save_point = transaction.savepoint()
            case = models.Case.objects.create(**request.data, creator=request.user.username)
            try:
                prepare.generate_casestep(body, case, request.user.username)
            except ObjectDoesNotExist:
                transaction.savepoint_rollback(save_point)
                return Response(response.CONFIG_MISSING)
        # 多余操作
        # case = models.Case.objects.filter(**request.data).first()

        # 不用多对多关系也能实现
        # case_step中的所有api_id
        # api_ids: set = prepare.generate_casestep(body, case, request.user.username)
        # apis = models.API.objects.filter(pk__in=api_ids).all()
        # case.apis.add(*apis)
        transaction.savepoint_commit(save_point)
        res = {"test_id": case.id}
        res.update(response.CASE_ADD_SUCCESS)
        return Response(res)

    @method_decorator(request_log(level="INFO"))
    def delete(self, request, **kwargs):
        """
        pk: test id delete single
        [{id:int}] delete batch
        """
        pk = kwargs.get("pk")

        try:
            if pk:
                prepare.case_end(pk)
            else:
                case_ids: list = []
                for content in request.data:
                    case_ids.append(content["id"])
                prepare.case_end(case_ids)

        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

        return Response(response.CASE_DELETE_SUCCESS)

    @method_decorator(request_log(level="INFO"))
    def put(self, request, **kwargs):
        # case_id
        pk = kwargs["pk"]

        # 在case_step表中找出case_id对应的所有记录,并且排除config
        api_id_list_of_dict = list(
            models.CaseStep.objects.filter(case_id=pk).exclude(method="config").values("source_api_id", "step")
        )

        # 通过source_api_id找到原来的api
        # 把原来api的name, body, url, method更新到case_step中
        for item in api_id_list_of_dict:
            source_api_id: int = item["source_api_id"]
            # 不存在api_id的直接跳过
            if source_api_id == 0:
                continue
            step: int = item["step"]
            source_api = models.API.objects.filter(pk=source_api_id).values("name", "body", "url", "method").first()
            if source_api is not None:
                models.CaseStep.objects.filter(case_id=pk, source_api_id=source_api_id, step=step).update(**source_api)
        models.Case.objects.filter(pk=pk).update(update_time=datetime.datetime.now())
        return Response(response.CASE_STEP_SYNC_SUCCESS)

    def update_tag(self, request):
        """
        批量更新用例类型
        """
        case_ids: list = request.data.get("case_ids", [])
        project_id: list = request.data.get("project_id", 0)
        tag: list = request.data.get("tag")
        models.Case.objects.filter(project_id=project_id, pk__in=case_ids).update(tag=tag)
        return Response(response.CASE_UPDATE_SUCCESS)


class CaseStepView(APIView):
    """
    测试用例step操作视图
    """

    @method_decorator(request_log(level="INFO"))
    def get(self, request, **kwargs):
        """
        返回用例集信息
        """
        pk = kwargs["pk"]

        queryset = models.CaseStep.objects.filter(case__id=pk).order_by("step")

        serializer = serializers.CaseStepSerializer(instance=queryset, many=True)

        resp = {
            "case": serializers.CaseSerializer(instance=models.Case.objects.get(id=pk), many=False).data,
            "step": serializer.data,
        }
        return Response(resp)
