import requests
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from FasterRunner import pagination
from extends import models
from fastrunner import models as fr_models
from fastrunner import serializers
from fastrunner.utils import (response, loader)
from fastrunner.utils.schedule import JobManager
from usermanager.models import UserInfo
from . import posetman
import simplejson


@api_view(['POST'])
def tansfer_postman_to_httprunner(request, **kwargs):
    project = kwargs.pop('id')
    upload_type = kwargs.pop('type')
    file = request.FILES['file']
    try:
        content = simplejson.load(file.file)
        if upload_type == 1:
            posetman.transfer_postman_cases_to_http_runner_cases(content, project)
        else:
            posetman.transfer_postman_environment_to_config(content, project)
    except Exception:
        return Response(response.FILE_UPLOAD_FAILURE)
    return Response(response.FILE_UPLOAD_SUCCESS)


class Task(GenericViewSet):
    queryset = models.Schedule.objects
    serializer_class = serializers.ScheduleSerializer
    pagination_class = pagination.MyPageNumberPagination

    def get_users(self, request):
        users = UserInfo.objects.values('id', 'username', 'email').all()
        return Response(users)

    """
        任务管理
    """

    @transaction.non_atomic_requests
    def add_job(self, request, **kwargs):
        if models.Schedule.objects.filter(name=request.data['name']).first():
            response.TASK_NAME_EXITS['name'] = request.data['name']
            return Response(response.TASK_NAME_EXITS)
        else:
            """
            反序列化
            """
            request.data['project'] = kwargs.pop('id')
            schedule_dto = serializers.ScheduleSerializer(data=request.data)
            if schedule_dto.is_valid(raise_exception=True):
                job = JobManager(request.data)
                job.add_job()
                schedule_dto.save()
                return Response(response.TASK_ADD_SUCCESS)
            else:
                return Response(response.SYSTEM_ERROR)

    def run_once(self, request, **kwargs):
        taskId = kwargs.pop('schedule_id')
        serializer = self.get_serializer(models.Schedule.objects.get(pk=taskId), many=False)
        JobManager(serializer.data).run_once()
        return Response(response.TASK_RUN_SUCCESS)

    @transaction.non_atomic_requests
    def delete_job(self, request, **kwargs):
        """
        删除定时任务
        """
        try:
            schedule = models.Schedule.objects.get(id=kwargs.get('schedule_id'))
            serializer = self.get_serializer(models.Schedule.objects.get(id=kwargs.get('schedule_id')), many=False)
            schedule.delete()
            JobManager(serializer.data).remove_job()
            return Response(response.TASK_DELETE_SUCCESS)
        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

    def modify_job(self, request, **kwargs):
        """
        修改job
        """
        pk = kwargs.get('schedule_id')
        schedule = models.Schedule.objects.get(pk=pk)
        cron = request.data.get('cron')
        try:
            schedule.cron = cron
            schedule.save()
            JobManager(self.get_serializer(schedule, many=False).data).modify()
            return Response(response.TASK_MODIFY_SUCCESS)
        except ObjectDoesNotExist:
            return Response(response.SYSTEM_ERROR)

    def list(self, request, **kwargs):
        tasks = self.get_queryset().filter(project_id=kwargs.pop('id')).order_by('-update_time')
        pagination_queryset = self.paginate_queryset(tasks)
        serializer = self.get_serializer(pagination_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class Report(GenericViewSet):
    serializer_class = serializers.ReportRelationSerializer
    pagination_class = pagination.MyPageNumberPagination

    def list(self, request, **kwargs):
        pk = kwargs.pop('id')
        self.queryset = fr_models.ReportRelation.objects.filter(project=pk).filter(
            ref=int(request.GET.get('ref')))
        historys = self.get_queryset().order_by(
            '-update_time')
        pagination_queryset = self.paginate_queryset(historys)
        serializer = self.get_serializer(pagination_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def get_reports(self, request, **kwargs):
        reports = fr_models.Report.objects.filter(reportRelation_id=int(request.GET.get('relation')),
                                                  refId=int(request.GET.get('ref'))).all()
        serializer = serializers.ReportSerializer(reports, many=True)
        return Response(serializer.data)


class LocustEnv(GenericViewSet):
    def add_locust_env(self, request, **kwargs):
        suite_id = kwargs.pop('id')
        config_id = request.data['params']['config']
        project = request.data['params']['project']
        progress = request.data['params']['progress']
        result_flag, port, msg = loader.gen_locust(suite_id, config_id, project, progress)
        if result_flag:
            response.LOCUST_ENV_ADD_SUCCESS['port'] = port
            return Response(response.LOCUST_ENV_ADD_SUCCESS)
        else:
            if port == -1:
                response.LOCUST_ENV_ADD_FAILURE_BUSY['msg'] = msg
                return Response(response.LOCUST_ENV_ADD_FAILURE_BUSY)
            else:
                response.LOCUST_ENV_ADD_FAILURE['port'] = port
                return Response(response.LOCUST_ENV_ADD_FAILURE)

    def get_locust_envs(self, request, **kwargs):
        project_id = kwargs.pop('id')
        return Response(loader.get_locusts(project_id))

    def remove_locust_env(self, request, **kwargs):
        id = kwargs.pop('id')
        flag, msg = loader.kill_task(id)
        if flag:
            return Response(response.LOCUST_ENV_DELETE_SUCCESS)
        else:
            response.LOCUST_ENV_DELETE_FAILURE['msg'] = msg
            return Response(response.LOCUST_ENV_DELETE_FAILURE)
