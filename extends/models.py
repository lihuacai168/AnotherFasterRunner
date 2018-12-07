from usermanager.models import BaseTable
from fastrunner.models import Project
from django.db import models


class Schedule(BaseTable):
    """
    定时任务表
    """
    # 报告发送策略 1分钟内不重复5次 一小时内不重复10次 一天内不重复15次
    sendStrategy = (
        (1, "不发送结果"),
        (2, "失败后发送"),
        (3, "不管怎样都发送结果")
    )

    class Meta:
        verbose_name = "定时任务"
        db_table = "Schedule"

    name = models.CharField("任务名称", unique=True, null=False, max_length=50)
    desc = models.CharField("描述", max_length=100, null=False)
    sendType = models.IntegerField("发送策略", choices=sendStrategy, default=1)
    cron = models.CharField("cron表达式", max_length=100, null=False)
    responsible = models.CharField("创建人", max_length=20, null=False)
    project = models.ForeignKey(Project, verbose_name='所属项目', null=False, on_delete=models.CASCADE)
    reportStrategy = models.IntegerField("发送报告策略", default=2, choices=sendStrategy)


class ScheduleReporter(BaseTable):
    """
    定时任务报告对象
    """

    class Meta:
        verbose_name = "定时任务报告对象"
        db_table = "ScheduleReporter"

    userId = models.IntegerField("用户id")
    userName = models.CharField("用户名", max_length=100)
    email = models.EmailField("邮箱")
    scheduleId = models.ForeignKey(Schedule, verbose_name='定时任务id', related_name='reporters', null=False,
                                   on_delete=models.CASCADE)


class ScheduleDetail(BaseTable):
    task_union = (
        (1, "api"),
        (2, "test_set"),
    )

    class Meta:
        verbose_name = "定时任务详细信息"
        db_table = "ScheduleDetail"

    stepId = models.IntegerField("任务对象id", null=False)
    stepName = models.CharField("任务名", max_length=100)
    stepRef = models.IntegerField("任务类型", choices=task_union)
    configId = models.IntegerField("配置id", null=False)
    scheduleId = models.ForeignKey(Schedule, verbose_name='定时任务id', null=False, related_name='details',
                                   on_delete=models.CASCADE)


class MockAPI(BaseTable):
    class Meta:
        verbose_name = "mockApi"
        db_table = "Mock"

    projectId = models.IntegerField("项目id", null=False, default=0)
    headers = models.CharField("返回的头对象", max_length=200, null=True)
    result = models.TextField("返回的对象", null=True)
