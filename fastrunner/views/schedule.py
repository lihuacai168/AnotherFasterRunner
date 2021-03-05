import json

from django.utils.decorators import method_decorator
from rest_framework.viewsets import GenericViewSet
from djcelery import models
from rest_framework.response import Response
from FasterRunner import pagination
from fastrunner import serializers
from fastrunner.utils import response
from fastrunner.utils.decorator import request_log
from fastrunner.utils.task import Task
from FasterRunner.mycelery import app


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
        request.data.update({"creator": request.user.username})
        task = Task(**request.data)
        resp = task.add_task()
        return Response(resp)

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

    @method_decorator(request_log(level='INFO'))
    def patch(self, request, **kwargs):
        """更新任务的状态
        :param request:
        :param kwargs:
        :return:
        """
        # {'pk': 22}
        task_obj = self.get_queryset().get(pk=kwargs['pk'])
        task_obj.enabled = request.data['switch']
        kwargs = json.loads(task_obj.kwargs)
        kwargs['updater'] = request.user.username
        task_obj.kwargs = json.dumps(kwargs, ensure_ascii=False)
        task_obj.save()
        return Response(response.TASK_UPDATE_SUCCESS)

    def delete(self, request, **kwargs):
        """删除任务
        """
        task = models.PeriodicTask.objects.get(id=kwargs["pk"])
        task.enabled = False
        task.delete()
        return Response(response.TASK_DEL_SUCCESS)

    @method_decorator(request_log(level='INFO'))
    def run(self, request, **kwargs):
        task = models.PeriodicTask.objects.get(id=kwargs["pk"])
        task_name = 'fastrunner.tasks.schedule_debug_suite'
        args = eval(task.args)
        kwargs = eval(task.kwargs)
        app.send_task(name=task_name, args=args, kwargs=kwargs)
        return Response(response.TASK_RUN_SUCCESS)

