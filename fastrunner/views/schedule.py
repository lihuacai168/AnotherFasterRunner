import json

from django.utils.decorators import method_decorator
from django_celery_beat import models
from rest_framework.viewsets import GenericViewSet
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

    @method_decorator(request_log(level="DEBUG"))
    def list(self, request):
        """
        查询项目信息
        """
        project = request.query_params.get("project")
        task_name = request.query_params.get("task_name")
        creator = request.query_params.get("creator")
        schedule = (
            self.get_queryset().filter(description=project).order_by("-date_changed")
        )
        if task_name:
            schedule = schedule.filter(name__contains=task_name)
        if creator:
            schedule = schedule.filter(kwargs__contains=f'"creator": "{creator}"')
        page_schedule = self.paginate_queryset(schedule)
        serializer = self.get_serializer(page_schedule, many=True)
        return self.get_paginated_response(serializer.data)

    @method_decorator(request_log(level="INFO"))
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
        re_gx = '(@(annually|yearly|monthly|weekly|daily|hourly|reboot))|(@every (\d+(ns|us|µs|ms|s|m|h))+)|((((\d+,)+\d+|(\d+(\/|-)\d+)|\d+|\*) ?){5,7})'
        ser = serializers.ScheduleDeSerializer(data=request.data)
        if ser.is_valid():
            request.data.update({"creator": request.user.username})
            match = re.match(re_gx, request.data.get("crontab"))
            if match is None:
                return Response({"code": "0101", "success": False, "msg": "定时任务表达式不符合规范"})
            task = Task(**request.data)
            resp = task.add_task()
            return Response(resp)
        else:
            return Response({"code": "0101", "success": False, "msg": "参数校验失败"})

    @method_decorator(request_log(level="INFO"))
    def copy(self, request, **kwargs):
        """复制定时任务"""
        task_obj = self.get_queryset().get(pk=kwargs["pk"])
        if task_obj.name == request.data["name"]:
            return Response(response.TASK_COPY_FAILURE)
        task_obj.id = None
        task_obj.name = request.data["name"]
        task_obj.total_run_count = 0
        kwargs = json.loads(task_obj.kwargs)
        kwargs["creator"] = request.user.username
        kwargs["updater"] = ""
        task_obj.kwargs = json.dumps(kwargs, ensure_ascii=False)
        task_obj.save()
        return Response(response.TASK_COPY_SUCCESS)

    @method_decorator(request_log(level="INFO"))
    def update(self, request, **kwargs):
        """更新任务
        :param request:
        :param kwargs:
        :return:
        """
        ser = serializers.ScheduleDeSerializer(data=request.data)
        if ser.is_valid():
            task = Task(**request.data)
            resp = task.update_task(kwargs["pk"])
            return Response(resp)
        else:
            return Response(response.TASK_CI_PROJECT_IDS_EXIST)

    @method_decorator(request_log(level="INFO"))
    def patch(self, request, **kwargs):
        """更新任务的状态
        :param request:
        :param kwargs:
        :return:
        """
        # {'pk': 22}
        task_obj = self.get_queryset().get(pk=kwargs["pk"])
        task_obj.enabled = request.data["switch"]
        kwargs = json.loads(task_obj.kwargs)
        kwargs["updater"] = request.user.username
        task_obj.kwargs = json.dumps(kwargs, ensure_ascii=False)
        task_obj.save()
        return Response(response.TASK_UPDATE_SUCCESS)

    def delete(self, request, **kwargs):
        """删除任务"""
        task = models.PeriodicTask.objects.get(id=kwargs["pk"])
        task.enabled = False
        task.delete()
        return Response(response.TASK_DEL_SUCCESS)

    @method_decorator(request_log(level="INFO"))
    def run(self, request, **kwargs):
        task = models.PeriodicTask.objects.get(id=kwargs["pk"])
        task_name = "fastrunner.tasks.schedule_debug_suite"
        args = eval(task.args)
        kwargs = json.loads(task.kwargs)
        kwargs["task_id"] = task.id
        app.send_task(name=task_name, args=args, kwargs=kwargs)
        return Response(response.TASK_RUN_SUCCESS)
