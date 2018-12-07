import logging
import enum
from apscheduler.events import *
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastrunner import models
from extends import models as etModels
from fastrunner.utils import loader, send
from fastrunner.serializers import ScheduleSerializer
import datetime
from datetime import datetime
from datetime import timedelta
from email.mime.text import MIMEText
import io, shutil


def get_date(days=None):
    return datetime.now() - timedelta(days=days)


class sendType(enum.Enum):
    not_send = 1
    err_send = 2
    all_send = 3


class JobManager:
    def __init__(self, data):
        self.__id = data.get('id')
        self.__name = data.get('name')
        self.__desc = data.get('desc')
        self.__crons = str(data.get('cron')).replace('?', '*').split()
        self.__responsible = data.get('responsible')
        self.__details = data.get('details')
        self.__reporters = data.get('reporters')
        self.__sendType = data.get('sendType')
        self.__projectId = data.get('project')

    def run_task(self):
        relation_id = models.ReportRelation.objects.create(
            name=self.__name,
            ref=3,
            project=self.__projectId,
            status="N/A"
        )
        flag = True
        contents = []
        for idx, detail in enumerate(self.__details):
            summary = None
            if detail.get('stepRef') == 1:
                api = models.API.objects.get(id=detail.get('stepId'))
                test_case = eval(api.body)
                summary = loader.debug_api(test_case, detail.get('configId'), api.project.id, loader.Run_type.SCHEDULE,
                                           detail["id"], self.__name, relation_id)
            elif detail.get('stepRef') == 2:
                test_list = models.CaseStep.objects. \
                    filter(case__id=detail.get('stepId')).order_by("step").values("body")

                test_case_list = []

                for content in test_list:
                    test_case_list.append(eval(content["body"]))

                    summary = loader.debug_api(test_case_list, detail.get('configId'),
                                               self.__projectId, loader.Run_type.SCHEDULE,
                                               detail["id"], self.__name, relation_id)
            reportContent = summary.pop('report_content')
            if self.__sendType == sendType.all_send.value:
                contents.append(reportContent)
            if self.__sendType == sendType.err_send.value and bool(summary['success']) == False:
                flag = False
                contents.append(reportContent)
        emails = []
        for report in self.__reporters:
            emails.append(report['email'])
        if self.__sendType == sendType.all_send.value:
            htmlContent = MIMEText(''.join(contents), _subtype='plain', _charset='utf-8')
            title = "FasterRunner定时任务日常报告-{}".format(self.__name)
            send.sendEmail(title, htmlContent, emails)
        elif self.__sendType == sendType.err_send.value:
            htmlContent = MIMEText(''.join(contents), _subtype='plain', _charset='utf-8')
            title = "FasterRunner定时任务错误报告-{}".format(self.__name)
            send.sendEmail(title, htmlContent, emails)

    def add_job(self):
        # 按照定时任务的类型来决定执行哪个方法
        """
             task_union = (
                (1, "api"),
                (2, "test_set"),
            )
        """
        if len(self.__crons) == 6:
            bs_schedule.add_job(id=self.__name,
                                func=self.run_task,
                                trigger='cron',
                                second=self.__crons[0],
                                minute=self.__crons[1],
                                hour=self.__crons[2],
                                day=self.__crons[3],
                                month=self.__crons[4],
                                year=self.__crons[5])
        else:
            bs_schedule.add_job(id=self.__name,
                                func=self.run_task,
                                trigger='cron',
                                second=self.__crons[0],
                                minute=self.__crons[1],
                                hour=self.__crons[2],
                                day=self.__crons[3],
                                month=self.__crons[4],
                                day_of_week=self.__crons[5],
                                year=self.__crons[6])

    def remove_job(self):
        try:
            bs_schedule.remove_job(job_id=self.__name)
        except JobLookupError:
            logging.debug("%{name}任务未找到！", self.__name)

    def run_once(self):
        self.run_task()

    def modify(self):
        try:
            job = bs_schedule.get_job(job_id=self.__name)
            if job is not None:
                job.modify(trigger=CronTrigger(
                    second=self.__crons[0],
                    minute=self.__crons[1],
                    hour=self.__crons[2],
                    day=self.__crons[3],
                    month=self.__crons[4],
                    day_of_week=self.__crons[5],
                    year=self.__crons[6]
                )
                )
        except JobLookupError:
            logging.debug("%{name}任务未找到！", self.__name)


JOB_DEFAULTS = {
    'misfire_grace_time': 1,
    'coalesce': False,
    'max_instances': 100
}

EXECUTORS = {
    'default': ThreadPoolExecutor(1),
    'processpool': ProcessPoolExecutor(4)
}

LISTENER_JOB = (EVENT_JOB_ADDED |
                EVENT_JOB_REMOVED |
                EVENT_JOB_MODIFIED |
                EVENT_JOB_EXECUTED |
                EVENT_JOB_ERROR |
                EVENT_JOB_MISSED)


def err_listener(events):
    if events.code == EVENT_JOB_MISSED:
        print("Job %s has missed." % str(events.job_id))
    if events.code == EVENT_JOB_ADDED:
        print("Job %s has added." % str(events.job_id))


bs_schedule = BackgroundScheduler(executors=EXECUTORS, job_defaults=JOB_DEFAULTS,
                                  timezone='Asia/Shanghai')
bs_schedule.add_listener(err_listener, LISTENER_JOB)


def clean_reports():
    models.ReportRelation.objects.filter(create_time__lte=get_date(7)).delete()


def schedule_init():
    data = ScheduleSerializer(etModels.Schedule.objects.all(), many=True).data
    bs_schedule.add_job(clean_reports, 'interval', hours=24)
    for i in data:
        JobManager(i).add_job()
    bs_schedule.start()


schedule_init()
