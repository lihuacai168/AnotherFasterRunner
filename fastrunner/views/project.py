from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from fastrunner import models, serializers
from FasterRunner import pagination
from rest_framework.response import Response
from fastrunner.utils import response
from fastrunner.utils import prepare
from fastrunner.utils import day
from fastrunner.utils.decorator import request_log
from fastrunner.utils.runner import DebugCode
from fastrunner.utils.tree import get_tree_max_id
from FasterRunner.auth import OnlyGetAuthenticator


class ProjectView(GenericViewSet):
    """
    项目增删改查
    """
    queryset = models.Project.objects.all().order_by('-update_time')
    serializer_class = serializers.ProjectSerializer
    pagination_class = pagination.MyCursorPagination

    @method_decorator(request_log(level='DEBUG'))
    def list(self, request):
        """
        查询项目信息
        """
        projects = self.get_queryset()
        page_projects = self.paginate_queryset(projects)
        serializer = self.get_serializer(page_projects, many=True)
        return self.get_paginated_response(serializer.data)

    @method_decorator(request_log(level='INFO'))
    def add(self, request):
        """添加项目 {
            name: str
        }
        """

        name = request.data["name"]

        if models.Project.objects.filter(name=name).first():
            response.PROJECT_EXISTS["name"] = name
            return Response(response.PROJECT_EXISTS)
        # 反序列化
        serializer = serializers.ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            project = models.Project.objects.get(name=name)
            prepare.project_init(project)
            return Response(response.PROJECT_ADD_SUCCESS)

        return Response(response.SYSTEM_ERROR)

    @method_decorator(request_log(level='INFO'))
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
        project.responsible = request.data['responsible']
        project.yapi_base_url = request.data['yapi_base_url']
        project.yapi_openapi_token = request.data['yapi_openapi_token']
        project.save()

        return Response(response.PROJECT_UPDATE_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def delete(self, request):
        """
        删除项目
        """
        if request.user.is_superuser is False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            project = models.Project.objects.get(id=request.data['id'])

            project.delete()
            prepare.project_end(project)

            return Response(response.PROJECT_DELETE_SUCCESS)
        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

    @method_decorator(request_log(level='INFO'))
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


class DebugTalkView(GenericViewSet):
    """
    DebugTalk update
    """
    # authentication_classes = [OnlyGetAuthenticator, ]
    serializer_class = serializers.DebugTalkSerializer

    @method_decorator(request_log(level='INFO'))
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

    @method_decorator(request_log(level='INFO'))
    def update(self, request):
        """
        编辑debugtalk.py 代码并保存
        """
        pk = request.data['id']
        try:
            models.Debugtalk.objects.filter(id=pk). \
                update(code=request.data['code'], updater=request.user.username)

        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

        return Response(response.DEBUGTALK_UPDATE_SUCCESS)

    @method_decorator(request_log(level='INFO'))
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

    # authentication_classes = [OnlyGetAuthenticator, ]

    @method_decorator(request_log(level='INFO'))
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

    @method_decorator(request_log(level='INFO'))
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


class VisitView(GenericViewSet):
    serializer_class = serializers.VisitSerializer
    queryset = models.Visit.objects

    def list(self, request):
        project = request.query_params.get("project")
        # 查询当前项目7天内的访问记录
        # 根据日期分组
        # 统计每天的条数
        count_data = self.get_queryset()\
            .filter(project=project, create_time__range=(day.get_day(-6), day.get_day(1)))\
            .extra(select={"create_time": "DATE_FORMAT(create_time,'%%m-%%d')"})\
            .values('create_time')\
            .annotate(counts=Count('id')).values('create_time', 'counts')

        create_time = []
        count = []
        for d in count_data:
            create_time.append(d['create_time'])
            count.append(d['counts'])
        return Response({'create_time': create_time, 'count': count})
#
# class FileView(APIView):
#
#     def post(self, request):
#         """
#         接收文件并保存
#         """
#         file = request.FILES['file']
#
#         if models.FileBinary.objects.filter(name=file.name).first():
#             return Response(response.FILE_EXISTS)
#
#         body = {
#             "name": file.name,
#             "body": file.file.read(),
#             "size": get_file_size(file.size)
#         }
#
#         models.FileBinary.objects.create(**body)
#
#         return Response(response.FILE_UPLOAD_SUCCESS)
