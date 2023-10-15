import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django_celery_beat.models import PeriodicTask
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from fastrunner.models import API, Case, Project, Report
from fastrunner.serializers import (ProjectSerializer, WarningListSerializer,
                                    get_cron_next_execute_time)

logger = logging.getLogger(__name__)


class ApiCountView(APIView):
    def get(self, request, *args, **kwargs):
        project_id: int = request.query_params.get("project", None)

        try:
            if project_id is not None:
                projects = [Project.objects.get(id=project_id)]
            else:
                projects = Project.objects.all()

            result = []
            total = 0

            for project in projects:
                # 查询该项目下所有API的数量（未删除的）
                api_count: int = API.objects.filter(project=project, delete=0).count()
                total += api_count

                # 计算API覆盖率
                api_cover_rate: str = ProjectSerializer().get_api_cover_rate(project)

                result.append(
                    {
                        "project_id": project.id,
                        "project_name": project.name,
                        "api_count": api_count,
                        "api_cover_rate": api_cover_rate,
                    }
                )

            return Response(
                {"result": result, "total": total}, status=status.HTTP_200_OK
            )

        except ObjectDoesNotExist:
            return Response({"error": "项目不存在"}, status=status.HTTP_404_NOT_FOUND)


class CaseCountView(APIView):
    def get(self, request, *args, **kwargs):
        project_id: int = request.query_params.get("project", None)

        try:
            if project_id is not None:
                projects = [Project.objects.get(id=project_id)]
            else:
                projects = Project.objects.all()

            result = []
            total = 0

            for project in projects:
                # 查询该项目下所有API的数量（未删除的）
                api_count: int = API.objects.filter(project=project, delete=0).count()

                # 查询该项目下所有用例的数量
                case_count: int = Case.objects.filter(project=project).count()
                total += case_count

                result.append(
                    {
                        "project_id": project.id,
                        "project_name": project.name,
                        "api_count": api_count,
                        "case_count": case_count,
                    }
                )

            return Response(
                {"result": result, "total": total}, status=status.HTTP_200_OK
            )

        except ObjectDoesNotExist:
            return Response({"error": "项目不存在"}, status=status.HTTP_404_NOT_FOUND)


class ScheduleListView(APIView):
    def get(self, request, *args, **kwargs):
        project_id: int = request.query_params.get("project", None)

        try:
            if project_id is not None:
                tasks = PeriodicTask.objects.filter(description=str(project_id))
            else:
                tasks = PeriodicTask.objects.all()

            result = []

            for task in tasks:
                if not task.description:
                    continue
                try:
                    project_id = task.description
                    project = Project.objects.get(id=project_id)
                    kwargs = json.loads(task.kwargs)
                except Exception:
                    logger.exception(
                        "project_id: %s, kwargs: %s",
                        project_id,
                        task.kwargs,
                        exc_info=True,
                    )
                    continue
                strategy = kwargs.get("strategy", "仅失败发送")

                result.append(
                    {
                        "id": task.id,
                        "project_id": project_id,
                        "project_name": project.name,
                        "task_name": task.name,
                        "next_execute_time": get_cron_next_execute_time(
                            kwargs["crontab"]
                        ),
                        "strategy": strategy,
                        "enabled": task.enabled,
                    }
                )

            return Response(result, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({"error": "项目或任务不存在"}, status=status.HTTP_404_NOT_FOUND)


class WarningListView(APIView):
    def get(self, request, *args, **kwargs):
        project_id: str = request.query_params.get("project", None)
        queryset = Report.objects.filter(type=3, status=0).order_by(
            "-create_time"
        )  # 默认查询所有项目

        # 数据校验和筛选
        if project_id is not None:
            try:
                project_id = int(project_id)
                queryset = queryset.filter(project_id=project_id)  # 如果有project_id，进一步筛选
            except ValueError:
                return Response(
                    {"error": "无效的项目ID"}, status=status.HTTP_400_BAD_REQUEST
                )

        # 序列化数据
        serializer = WarningListSerializer(queryset, many=True)
        return Response(serializer.data)
