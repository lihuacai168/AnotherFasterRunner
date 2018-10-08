from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from fastrunner import models, serializers
from FasterRunner import pagination
from rest_framework.response import Response
from fastrunner.utils import response
from fastrunner.utils import prepare
from fastrunner.utils.parser import Format, Parse
from fastrunner.utils.runner import DebugCode
from fastrunner.utils.tree import get_tree_max_id
from fastrunner.utils import loader
from django.db import DataError


# Create your views here.


class ProjectView(GenericViewSet):
    """
    项目增删改查
    """

    queryset = models.Project.objects.all().order_by('-update_time')
    serializer_class = serializers.ProjectSerializer
    pagination_class = pagination.MyCursorPagination

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

    def single(self, request, **kwargs):
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
    pagination_class = pagination.MyCursorPagination
    serializer_class = serializers.DataBaseSerializer


class DebugTalkView(GenericViewSet):
    """
    DebugTalk update
    """
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
                update(code=request.data['code'])

        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

        return Response(response.DEBUGTALK_UPDATE_SUCCESS)

    def run(self, request):
        try:
            code = request.data["code"]
        except KeyError:
            return Response(response.KEY_MISS)
        debug = DebugCode(code)
        debug.run()
        resp = {
            "msg": debug.resp,
            "success": True,
            "code": "0001"
        }
        return Response(resp)


class TreeView(APIView):
    """
    树形结构操作
    """

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

    def post(self, request):
        """
        接收文件并保存
        """
        file = request.FILES['file']
        body = {
            "name": file.name,
            "body": file.file.read(),
            "size": file.size,
            "relation": 1
        }

        # models.FileBinary.objects.create(**body)

        return Response(response.FILE_UPLOAD_SUCCESS)


class APITemplateView(GenericViewSet):
    """
    API操作视图
    """
    serializer_class = serializers.APISerializer
    queryset = models.API.objects
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

        queryset = self.get_queryset().filter(project__id=project, relation=node).order_by('-update_time')
        pagination_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pagination_queryset, many=True)

        return self.get_paginated_response(serializer.data)

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

        if "case" in body[0].keys():
            case_info = body[0]["case"]
        else:
            case_info = body[0]

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


class ConfigView(GenericViewSet):
    serializer_class = serializers.ConfigSerializer
    queryset = models.Config.objects

    def list(self, request):
        project = request.query_params['project']
        queryset = self.get_queryset().filter(project__id=project).order_by('-update_time')
        pagination_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pagination_queryset, many=True)

        return self.get_paginated_response(serializer.data)

    def all(self, request, **kwargs):
        """
        get all config
        """
        pk = kwargs["pk"]

        queryset = self.get_queryset().filter(project__id=pk). \
            order_by('-update_time').values("id", "name")

        return Response(queryset)

    def add(self, request):
        """
            add new config
            {
                name: str
                project: int
                body: dict
            }
        """

        config = Format(request.data, level='config')
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
            "project": config.project
        }

        models.Config.objects.create(**config_body)
        return Response(response.CONFIG_ADD_SUCCESS)

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
        pk = kwargs['pk']

        try:
            config = models.Config.objects.get(id=pk)

        except ObjectDoesNotExist:
            return Response(response.CONFIG_NOT_EXISTS)

        format = Format(request.data, level="config")
        format.parse()

        if models.Config.objects.exclude(id=pk).filter(name=format.name).first():
            return Response(response.CONFIG_EXISTS)

        config.name = format.name
        config.body = format.testcase
        config.base_url = format.base_url
        config.save()

        return Response(response.CONFIG_UPDATE_SUCCESS)

    def copy(self, request, **kwargs):
        """
        pk: int
        {
            name: str
        }
        """
        pk = kwargs['pk']
        try:
            config = models.Config.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(response.CONFIG_NOT_EXISTS)

        if models.Config.objects.filter(**request.data).first():
            return Response(response.CONFIG_EXISTS)

        config.id = None

        body = eval(config.body)
        name = request.data['name']

        body['name'] = name
        config.name = name
        config.body = body
        config.save()

        return Response(response.CONFIG_ADD_SUCCESS)

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
                models.Config.objects.get(id=kwargs['pk']).delete()
            else:
                for content in request.data:
                    models.Config.objects.get(id=content['id']).delete()

        except ObjectDoesNotExist:
            return Response(response.CONFIG_NOT_EXISTS)

        return Response(response.API_DEL_SUCCESS)


@api_view(['POST'])
def run_api(request):
    """ run api by body and config
    """
    config = request.data.pop("config")
    api = Format(request.data)
    api.parse()

    summary = loader.debug_api(api.testcase, config, api.project)

    return Response(summary)


@api_view(['GET'])
def run_api_pk(request, **kwargs):
    """run api by pk and config
    """
    api = models.API.objects.get(id=kwargs['pk'])
    testcase = eval(api.body)

    summary = loader.debug_api(testcase, request.query_params["config"], api.project.id)

    return Response(summary)


@api_view(['POST'])
def run_api_tree(request):
    """run api by tree
    {
        project: int
        relation: int
        config: int
    }
    """
    # order by id default
    project = request.data['project']
    api = models.API.objects. \
        filter(project__id=project, relation=request.data['relation']). \
        order_by('id').values('body')

    testcase = []
    for content in api:
        testcase.append(eval(content['body']))

    summary = loader.debug_api(testcase, request.data["config"], project)

    return Response(summary)


@api_view(["POST"])
def run_testsuite(request):
    """debug testsuite
    {
        name: str,
        config: int
        body: dict
    }
    """
    body = request.data["body"]

    testcase_list = []

    for test in body:
        testcase_list.append(loader.load_test(test))

    summary = loader.debug_api(testcase_list, request.data['config'], request.data["project"])
    return Response(summary)


@api_view(["POST"])
def run_test(request):
    """debug single test
    {
        config: int
        body: dict
    }
    """

    body = request.data["body"]
    summary = loader.debug_api(loader.load_test(body), request.data["config"], request.data["project"])
    return Response(summary)


@api_view(["GET"])
def run_testsuite_pk(request, **kwargs):
    """run testsuite by pk
        pk: int
        config: int
    """
    pk = kwargs["pk"]

    test_list = models.CaseStep.objects.\
        filter(case__id=pk).order_by("step").values("body")

    testcase_list = []

    for content in test_list:
        testcase_list.append(eval(content["body"]))

    summary = loader.debug_api(testcase_list, request.query_params["config"], request.query_params["project"])

    return Response(summary)
