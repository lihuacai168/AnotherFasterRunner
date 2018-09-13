from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from fastrunner import models, serializers
from FasterRunner import pagination
from rest_framework.response import Response
from fastrunner.utils import response
from fastrunner.utils import prepare
from fastrunner.utils.parser import Format, Parse
from fastrunner.utils.tree import get_tree_max_id
from django.db import DataError


# Create your views here.


class ProjectView(GenericViewSet):
    """
    项目增删改查
    """

    queryset = models.Project.objects.all().order_by('-update_time')
    serializer_class = serializers.ProjectSerializer
    pagination_class = pagination.MyCursorPagination
    authentication_classes = ()

    def list(self, request):
        """
        查询项目信息
        """

        projects = self.get_queryset()
        page_projects = self.paginate_queryset(projects)
        serializer = self.get_serializer(page_projects, many=True)
        return self.get_paginated_response(serializer.data)

    def add(self, request):
        """
        添加项目
        """

        name = request.data["name"]

        if models.Project.objects.filter(name=name).first():
            response.PROJECT_EXISTS["name"] = name
            return Response(response.PROJECT_EXISTS)
        """
        反序列化
        """
        serializer = serializers.ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            project = models.Project.objects.get(name=name)
            prepare.project_init(project)
            return Response(response.PROJECT_ADD_SUCCESS)

        else:
            return Response(response.SYSTEM_ERROR)

    def update(self, request):
        """
        编辑项目
        """

        try:
            project = models.Project.objects.get(id=request.data['id'])
        except (KeyError, ObjectDoesNotExist):
            return Response(response.SYSTEM_ERROR)

        if request.data['name'] != project.name:
            if models.Project.objects.filter(name=request.data['name']).first():
                return Response(response.PROJECT_EXISTS)

        # 调用save方法update_time字段才会自动更新
        project.name = request.data['name']
        project.desc = request.data['desc']
        project.save()

        return Response(response.PROJECT_UPDATE_SUCCESS)

    def delete(self, request):
        """
        删除项目
        """
        try:
            project = models.Project.objects.get(id=request.data['id'])

            project.delete()
            prepare.project_end(project)

            return Response(response.PROJECT_DELETE_SUCCESS)
        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

    def get_single(self, request, **kwargs):
        """
        得到单个项目相关统计信息
        """
        pk = kwargs.pop('pk')
        try:
            queryset = models.Project.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(response.PROJECT_NOT_EXISTS)

        serializer = self.get_serializer(queryset, many=False)

        project_info = prepare.get_project_detail(pk)
        project_info.update(serializer.data)

        return Response(project_info)





class DataBaseView(ModelViewSet):
    """
    DataBase 增删改查
    """
    queryset = models.DataBase.objects.all().order_by('-update_time')
    authentication_classes = ()
    pagination_class = pagination.MyCursorPagination
    serializer_class = serializers.DataBaseSerializer


class DebugTalkView(GenericViewSet):
    """
    DebugTalk update
    """
    authentication_classes = ()
    serializer_class = serializers.DebugTalkSerializer

    def debugtalk(self, request, **kwargs):
        """
        得到debugtalk code
        """
        pk = kwargs.pop('pk')
        try:
            queryset = models.Debugtalk.objects.get(project__id=pk)
        except ObjectDoesNotExist:
            return Response(response.DEBUGTALK_NOT_EXISTS)

        serializer = self.get_serializer(queryset, many=False)

        return Response(serializer.data)

    def update(self, request):
        """
        编辑debugtalk.py 代码并保存
        """
        pk = request.data['id']
        try:
            models.Debugtalk.objects.filter(id=pk). \
                update(debugtalk=request.data['debugtalk'])

        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

        return Response(response.DEBUGTALK_UPDATE_SUCCESS)


class TreeView(APIView):
    """
    树形结构操作
    """
    authentication_classes = ()

    def get(self, request, **kwargs):
        """
        返回树形结构
        当前最带节点ID
        """

        try:
            tree_type = request.query_params['type']
            tree = models.Relation.objects.get(project__id=kwargs['pk'], type=tree_type)
        except KeyError:
            return Response(response.KEY_MISS)

        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

        body = eval(tree.tree)  # list
        tree = {
            "tree": body,
            "id": tree.id,
            "success": True,
            "max": get_tree_max_id(body)
        }
        return Response(tree)

    def patch(self, request, **kwargs):
        """
        修改树形结构，ID不能重复
        """
        try:
            body = request.data['body']
            mode = request.data['mode']

            relation = models.Relation.objects.get(id=kwargs['pk'])
            relation.tree = body
            relation.save()

        except KeyError:
            return Response(response.KEY_MISS)

        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

        #  mode -> True remove node
        if mode:
            prepare.tree_end(request.data, relation.project)

        response.TREE_UPDATE_SUCCESS['tree'] = body
        response.TREE_UPDATE_SUCCESS['max'] = get_tree_max_id(body)

        return Response(response.TREE_UPDATE_SUCCESS)


class FileView(APIView):
    authentication_classes = ()

    def post(self, request):
        """
        接收文件并保存
        """
        file = request.FILES['file']

        # 此处应该插入数据库
        pass

        return Response(response.FILE_UPLOAD_SUCCESS)


class APITemplateView(GenericViewSet):
    """
    API操作视图
    """
    authentication_classes = ()
    serializer_class = serializers.APISerializer
    """使用默认分页器"""

    def list(self, request):
        """
        接口列表 {
            project: int,
            node: int
        }
        """

        node = request.query_params["node"]
        project = request.query_params["project"]

        queryset = models.API.objects.filter(project__id=project)

        if node == '':
            queryset = queryset.order_by('-update_time')
        else:
            queryset = queryset.filter(relation=node).order_by('-update_time')

        pagination_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pagination_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def add(self, request):
        """
        新增一个接口
        """

        api = Format(request.data)
        api.parse_test()

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

    def update(self, request, **kwargs):
        """
        更新接口
        """
        pk = kwargs['pk']
        api = Format(request.data)
        api.parse_test()

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
                models.API.objects.get(id=kwargs['pk']).delete()
            else:
                for content in request.data:
                    models.API.objects.get(id=content['id']).delete()

        except ObjectDoesNotExist:
            return Response(response.API_NOT_FOUND)

        return Response(response.API_DEL_SUCCESS)

    def get_single(self, request, **kwargs):
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


class TestCaseView(GenericViewSet):
    authentication_classes = ()

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

        queryset = models.Case.objects.filter(project__id=project)

        # update_time 降序排列
        if node == '':
            queryset = queryset.order_by('-update_time')
        else:
            queryset = queryset.filter(relation=node).order_by('-update_time')

        pagination_query = pagination.MyPageNumberPagination().paginate_queryset(queryset, request)

        serializer = serializers.CaseSerializer(instance=pagination_query, many=True)

        return Response(serializer.data)

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

    def post(self, request):
        """
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
    authentication_classes = ()

    def get(self, request, **kwargs):
        """
        返回用例集信息
        """
        pk = kwargs['pk']

        queryset = models.CaseStep.objects.filter(case__id=pk).order_by('step')

        serializer = serializers.CaseStepSerializer(instance=queryset, many=True)

        return Response(serializer.data)