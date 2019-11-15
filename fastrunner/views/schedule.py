from django.utils.decorators import method_decorator
from rest_framework.viewsets import GenericViewSet
from djcelery import models
from rest_framework.response import Response
from FasterRunner import pagination
from fastrunner import serializers
from fastrunner.utils import response
from fastrunner.utils.decorator import request_log
from fastrunner.utils.task import Task


class ScheduleView(GenericViewSet):
    """
    定时任务增删改查
    """
    queryset = models.PeriodicTask.objects
    serializer_class = serializers.PeriodicTaskSerializer
    pagination_class = pagination.MyPageNumberPagination

    @method_decorator(request_log(level='DEBUG'))
    def list(self, request):
        """
        查询项目信息
        """
        project = request.query_params.get("project")
        schedule = self.get_queryset().filter(description=project).order_by('-date_changed')
        page_schedule = self.paginate_queryset(schedule)
        serializer = self.get_serializer(page_schedule, many=True)
        return self.get_paginated_response(serializer.data)

    @method_decorator(request_log(level='INFO'))
    def add(self, request):
        """新增定时任务{
            name: str
            crontab: str
            switch: bool
            data: [int,int]
            strategy: str
            receiver: str
            copy: str
            project: int
        }
        """
        task = Task(**request.data)
        resp = task.add_task()
        return Response(resp)

    # def update(self,request):
    #     task = Task(**request.data)
    #     resp = 1

    #
    # @method_decorator(request_log(level='INFO'))
    # def update(self, request):
    #     """
    #     编辑项目
    #     """
    #
    #     try:
    #         project = models.Project.objects.get(id=request.data['id'])
    #     except (KeyError, ObjectDoesNotExist):
    #         return Response(response.SYSTEM_ERROR)
    #
    #     if request.data['name'] != project.name:
    #         if models.Project.objects.filter(name=request.data['name']).first():
    #             return Response(response.PROJECT_EXISTS)
    #
    #     # 调用save方法update_time字段才会自动更新
    #     project.name = request.data['name']
    #     project.desc = request.data['desc']
    #     project.save()
    #
    #     return Response(response.PROJECT_UPDATE_SUCCESS)
    #
    # @method_decorator(request_log(level='INFO'))

    @method_decorator(request_log(level='INFO'))
    def update(self, request, **kwargs):
        """更新任务
        :param request:
        :param kwargs:
        :return:
        """
        task = Task(**request.data)
        resp = task.update_task(kwargs['pk'])
        return Response(resp)

    def delete(self, request, **kwargs):
        """删除任务
        """
        task = models.PeriodicTask.objects.get(id=kwargs["pk"])
        task.enabled = False
        task.delete()
        return Response(response.TASK_DEL_SUCCESS)