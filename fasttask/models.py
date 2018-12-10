from django.db import models

# Create your models here.
from fastrunner.models import Project
from fastuser.models import BaseTable


class Schedule(BaseTable):
    """
    定时任务信息表
    """

    send_strategy = (
        (1, "不发送结果"),
        (2, "失败后发送"),
        (3, "不管怎样都发送结果")
    )

    triggers_type = (
        (1, "间隔调度"),
        (2, "crontab表达式")
    )

    class Meta:
        verbose_name = "定时任务"
        db_table = "Schedule"

    name = models.CharField("项目名称", unique=True, null=False, max_length=100)
    desc = models.CharField("简要介绍", max_length=100, null=False)
    send_type = models.IntegerField("发送策略", choices=send_strategy, default=1)
    triggers = models.IntegerField("触发器", choices=triggers_type, default=1)
    crontab = models.CharField("时间配置", max_length=100, null=False)
    creator = models.CharField("创建者", max_length=50)
    project = models.ForeignKey(Project, verbose_name='所属项目', null=False, on_delete=models.CASCADE)


class ScheduleReporter(BaseTable):
    """
    定时任务报告对象
    """

    class Meta:
        verbose_name = "定时任务报告对象"
        db_table = "ScheduleReporter"

    receive = models.EmailField("接收人", null=True)
    copy = models.EmailField("抄送人", null=True)
    schedule = models.ForeignKey(Schedule, verbose_name='定时任务', on_delete=models.CASCADE)


class ScheduleDetail(BaseTable):
    task_union = (
        (1, "api"),
        (2, "test_suite"),
    )

    class Meta:
        verbose_name = "定时任务详细信息"
        db_table = "ScheduleDetail"

    type = models.IntegerField("任务类型", choices=task_union)
    config = models.IntegerField("配置id", null=True)
    tree = models.TextField("运行目录", null=False)
    schedule = models.ForeignKey(Schedule, verbose_name='定时任务', on_delete=models.CASCADE)
