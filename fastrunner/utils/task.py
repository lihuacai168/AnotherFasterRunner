import json
from loguru import logger
from django_celery_beat import models as celery_models
from fastrunner.utils import response
from fastrunner.utils.parser import format_json


class Task(object):
    """
    定时任务操作
    """

    def __init__(self, **kwargs):
        logger.info(
            "before process task data:\n {kwargs}".format(kwargs=format_json(kwargs))
        )
        self.__name = kwargs["name"]
        self.__data = kwargs["data"]
        self.__crontab = kwargs["crontab"]
        self.__switch = kwargs["switch"]
        self.__task = "fastrunner.tasks.schedule_debug_suite"
        self.__project = kwargs["project"]
        self.__email = {
            "strategy": kwargs["strategy"],
            "mail_cc": kwargs.get("mail_cc"),
            "receiver": kwargs.get("receiver"),
            "crontab": self.__crontab,
            "project": self.__project,
            "task_name": self.__name,
            "webhook": kwargs["webhook"],
            "updater": kwargs.get("updater"),
            "creator": kwargs.get("creator"),
            "ci_project_ids": kwargs.get("ci_project_ids", []),
            "ci_env": kwargs.get("ci_env", "请选择"),
            "is_parallel": kwargs.get("is_parallel", False),
            "config": kwargs.get("config", "请选择"),
        }
        self.__crontab_time = None

    def format_crontab(self):
        """
        格式化时间
        """
        crontab = self.__crontab.split(" ")
        if len(crontab) > 5:
            return response.TASK_TIME_ILLEGAL
        try:
            self.__crontab_time = {
                "day_of_week": crontab[4],
                "month_of_year": crontab[3],
                "day_of_month": crontab[2],
                "hour": crontab[1],
                "minute": crontab[0],
            }
        except Exception:
            return response.TASK_TIME_ILLEGAL

        return response.TASK_ADD_SUCCESS

    def add_task(self):
        """
        add tasks
        """
        if (
            celery_models.PeriodicTask.objects.filter(name__exact=self.__name).count()
            > 0
        ):
            logger.info("{name} tasks exist".format(name=self.__name))
            return response.TASK_HAS_EXISTS

        if self.__email["strategy"] == "始终发送" or self.__email["strategy"] == "仅失败发送":
            if self.__email["receiver"] == "":
                # return response.TASK_EMAIL_ILLEGAL
                pass

        resp = self.format_crontab()
        if resp["success"]:
            crontab = celery_models.CrontabSchedule.objects.filter(
                **self.__crontab_time
            ).first()
            if crontab is None:
                crontab = celery_models.CrontabSchedule.objects.create(
                    **self.__crontab_time
                )
            task, created = celery_models.PeriodicTask.objects.get_or_create(
                name=self.__name, task=self.__task, crontab=crontab
            )
            task.crontab = crontab
            task.enabled = self.__switch
            task.args = json.dumps(self.__data, ensure_ascii=False)
            task.kwargs = json.dumps(self.__email, ensure_ascii=False)
            task.description = self.__project
            task.save()
            logger.info("{name} tasks save success".format(name=self.__name))
            return response.TASK_ADD_SUCCESS
        else:
            return resp

    def update_task(self, pk):
        resp = self.format_crontab()
        if resp["success"]:
            task = celery_models.PeriodicTask.objects.get(id=pk)
            crontab = celery_models.CrontabSchedule.objects.filter(
                **self.__crontab_time
            ).first()
            if crontab is None:
                crontab = celery_models.CrontabSchedule.objects.create(
                    **self.__crontab_time
                )
            task.crontab = crontab
            task.enabled = self.__switch
            task.args = json.dumps(self.__data, ensure_ascii=False)
            task.kwargs = json.dumps(self.__email, ensure_ascii=False)
            task.description = self.__project
            task.name = self.__name
            task.save()
            logger.info("{name} tasks save success".format(name=self.__name))
            return response.TASK_UPDATE_SUCCESS
        else:
            return resp
