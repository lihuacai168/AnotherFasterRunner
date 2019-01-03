from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from fastrunner import models, serializers

from rest_framework.response import Response
from fastrunner.utils import response
from fastrunner.utils import prepare


class TestCaseView(GenericViewSet):
    queryset = models.Case.objects
    serializer_class = serializers.CaseSerializer

    def get(self, request):
        """
        查询指定CASE列表，不包含CASE STEP
        {
            "project": int,
            "node": int
        }
        """
        node = request.query_params["node"]
        project = request.query_params["project"]

        # update_time 降序排列
        queryset = self.get_queryset().filter(project__id=project, relation=node).order_by('-update_time')

        pagination_query = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pagination_query, many=True)

        return self.get_paginated_response(serializer.data)

    def copy(self, request, **kwargs):
        """
        pk int: test id
        {
            name: test name
            relation: int
            project: int
        }
        """
        pk = kwargs['pk']

        if models.Case.objects.filter(**request.data).first():
            return Response(response.CASE_EXISTS)

        case = models.Case.objects.get(id=pk)
        case.id = None
        case.name = request.data['name']
        case.save()

        case_step = models.CaseStep.objects.filter(case__id=pk)

        for step in case_step:
            step.id = None
            step.case = models.Case.objects.get(name=request.data['name'])
            step.save()

        return Response(response.CASE_ADD_SUCCESS)

    def patch(self, request, **kwargs):
        """
        更新测试用例集
        {
            name: str
            id: int
            body: []
        }
        """

        pk = kwargs['pk']

        body = request.data.pop('body')

        if "case" in body[-1].keys():
            case_info = body[-1]["case"]
        else:
            case_info = body[-1]

        if models.Case.objects.exclude(id=pk). \
                filter(name=request.data['name'],
                       project__id=case_info["project"],
                       relation=case_info["relation"]).first():
            return Response(response.CASE_EXISTS)

        case = models.Case.objects.get(id=pk)

        prepare.update_casestep(body, case)

        models.Case.objects.filter(id=pk).update(**request.data)

        return Response(response.CASE_UPDATE_SUCCESS)

    def post(self, request):
        """
        新增测试用例集
        {
            name: str
            project: int,
            relation: int,
            body: [{
                id: int,
                project: int,
                name: str,
                method: str,
                url: str
            }]
        }
        """

        try:
            pk = request.data['project']
            request.data['project'] = models.Project.objects.get(id=pk)

        except KeyError:
            return Response(response.KEY_MISS)

        except ObjectDoesNotExist:
            return Response(response.PROJECT_NOT_EXISTS)

        body = request.data.pop('body')

        # 同一项目同一节点下存在相同用例集
        if models.Case.objects.filter(**request.data).first():
            return Response(response.CASE_EXISTS)

        models.Case.objects.create(**request.data)

        case = models.Case.objects.filter(**request.data).first()

        prepare.generate_casestep(body, case)

        return Response(response.CASE_ADD_SUCCESS)

    def delete(self, request, **kwargs):
        """
        pk: test id delete single
        [{id:int}] delete batch
        """
        pk = kwargs.get('pk')

        try:
            if pk:
                prepare.case_end(pk)
            else:
                for content in request.data:
                    prepare.case_end(content['id'])

        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

        return Response(response.CASE_DELETE_SUCCESS)


class CaseStepView(APIView):
    """
    测试用例step操作视图
    """

    def get(self, request, **kwargs):
        """
        返回用例集信息
        """
        pk = kwargs['pk']

        queryset = models.CaseStep.objects.filter(case__id=pk).order_by('step')

        serializer = serializers.CaseStepSerializer(instance=queryset, many=True)

        return Response(serializer.data)
