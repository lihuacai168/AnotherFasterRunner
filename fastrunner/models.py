import jsonfield
from django.db import models
from django_celery_beat.models import PeriodicTask


# Create your models here.
from model_utils import Choices

from fastuser.models import BaseTable


class Project(BaseTable):
    """
    项目信息表
    """

    class Meta:
        verbose_name = "项目信息"
        db_table = "project"

    name = models.CharField(
        "项目名称", unique=True, null=False, max_length=100
    )
    desc = models.CharField("简要介绍", max_length=100, null=False)
    responsible = models.CharField("创建人", max_length=20, null=False)
    yapi_base_url = models.CharField(
        "yapi的openapi url", max_length=100, null=False, default="", blank=True
    )
    yapi_openapi_token = models.CharField(
        "yapi openapi的token",
        max_length=128,
        null=False,
        default="",
        blank=True,
    )
    # jira相关的
    jira_project_key = models.CharField(
        "jira项目key", null=False, default="", max_length=30, blank=True
    )
    jira_bearer_token = models.CharField(
        "jira bearer_token", null=False, default="", max_length=45, blank=True
    )
    is_deleted = models.IntegerField("是否删除", null=True, default=0)


class Debugtalk(BaseTable):
    """
    驱动文件表
    """

    class Meta:
        verbose_name = "驱动库"
        db_table = "debugtalk"

    code = models.TextField(
        "python代码", default="# write you code", null=False
    )
    project = models.OneToOneField(
        to=Project, on_delete=models.CASCADE, db_constraint=False
    )


class Config(BaseTable):
    """
    环境信息表
    """

    class Meta:
        verbose_name = "环境信息"
        db_table = "config"

    name = models.CharField("环境名称", null=False, max_length=100)
    body = models.TextField("主体信息", null=False)
    base_url = models.CharField("请求地址", null=False, max_length=100)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, db_constraint=False
    )
    is_default = models.BooleanField("默认配置", default=False)


class API(BaseTable):
    """
    API信息表
    """

    class Meta:
        verbose_name = "接口信息"
        db_table = "api"

    ENV_TYPE = ((0, "测试环境"), (1, "生产环境"), (2, "预发布 "))
    TAG = Choices(
        (0, "未知"),
        (1, "成功"),
        (2, "失败"),
        (3, "自动成功"),
        (4, "废弃"),
    )
    name = models.CharField(
        "接口名称", null=False, max_length=100, db_index=True
    )
    body = models.TextField("主体信息", null=False)
    url = models.CharField(
        "请求地址", null=False, max_length=255, db_index=True
    )
    method = models.CharField("请求方式", null=False, max_length=10)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, db_constraint=False
    )
    relation = models.IntegerField("节点id", null=False)
    delete = models.IntegerField("是否删除", null=True, default=0)
    rig_id = models.IntegerField("网关API_id", null=True, db_index=True)
    rig_env = models.IntegerField("网关环境", choices=ENV_TYPE, default=0)
    tag = models.IntegerField("API标签", choices=TAG, default=0)
    # yapi相关的
    yapi_catid = models.IntegerField("yapi的分组id", null=True, default=0)
    yapi_id = models.IntegerField("yapi的id", null=True, default=0)
    ypai_add_time = models.CharField(
        "yapi创建时间", null=True, default="", max_length=10
    )
    ypai_up_time = models.CharField(
        "yapi更新时间", null=True, default="", max_length=10
    )
    ypai_username = models.CharField(
        "yapi的原作者", null=True, default="", max_length=30
    )
    # resp_sample = models.TextField("接口响应样例", default='{}', null=False)


class Case(BaseTable):
    """
    用例信息表
    """

    class Meta:
        verbose_name = "用例信息"
        db_table = "case"

    tag = (
        (1, "冒烟用例"),
        (2, "集成用例"),
        (3, "监控脚本"),
        (4, "核心用例"),
    )
    name = models.CharField("用例名称", null=False, max_length=100)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, db_constraint=False
    )
    relation = models.IntegerField("节点id", null=False)
    length = models.IntegerField("API个数", null=False)
    tag = models.IntegerField("用例标签", choices=tag, default=2)
    # apis = models.ManyToManyField(API, db_table='api_case', related_name='api_case_relate')

    @property
    def tasks(self):
        task_objs = PeriodicTask.objects.filter(
            description=self.project.id
        ).values("id", "name", "args")
        return filter(
            lambda task: self.id in eval(task.pop("args")), task_objs
        )


class CaseStep(BaseTable):
    """
    Test Case Step
    """

    class Meta:
        verbose_name = "用例信息 Step"
        db_table = "case_step"

    name = models.CharField("用例名称", null=False, max_length=100)
    body = models.TextField("主体信息", null=False)
    url = models.CharField("请求地址", null=False, max_length=255)
    method = models.CharField("请求方式", null=False, max_length=10)
    case = models.ForeignKey(
        Case, on_delete=models.CASCADE, db_constraint=False
    )
    step = models.IntegerField("顺序", null=False)
    source_api_id = models.IntegerField("api来源", null=False)


class HostIP(BaseTable):
    """
    全局变量
    """

    class Meta:
        verbose_name = "HOST配置"
        db_table = "host_ip"

    name = models.CharField(null=False, max_length=100)
    value = models.TextField(null=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, db_constraint=False
    )


class Variables(BaseTable):
    """
    全局变量
    """

    class Meta:
        verbose_name = "全局变量"
        db_table = "variables"

    key = models.CharField(null=False, max_length=100)
    value = models.CharField(null=False, max_length=1024)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, db_constraint=False
    )
    description = models.CharField("全局变量描述", null=True, max_length=100)


class Report(BaseTable):
    """
    报告存储
    """

    report_type = (
        (1, "调试"),
        (2, "异步"),
        (3, "定时"),
        (4, "部署"),
    )
    report_status = (
        (0, "失败"),
        (1, "成功"),
    )

    class Meta:
        verbose_name = "测试报告"
        db_table = "report"

    name = models.CharField("报告名称", null=False, max_length=100)
    type = models.IntegerField("报告类型", choices=report_type)
    status = models.BooleanField("报告状态", choices=report_status, blank=True)
    summary = models.TextField("报告基础信息", null=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, db_constraint=False
    )
    ci_metadata = jsonfield.JSONField()
    ci_project_id = models.IntegerField(
        "gitlab的项目id", default=0, null=True, db_index=True
    )
    ci_job_id = models.CharField(
        "gitlab的项目id",
        unique=True,
        null=True,
        default=None,
        db_index=True,
        max_length=15,
    )

    @property
    def ci_job_url(self):
        if self.ci_metadata:
            return self.ci_metadata.get("ci_job_url")
        return ""


class ReportDetail(models.Model):
    class Meta:
        verbose_name = "测试报告详情"
        db_table = "report_detail"

    report = models.OneToOneField(
        Report, on_delete=models.CASCADE, null=True, db_constraint=False
    )
    summary_detail = models.TextField("报告详细信息")


class Relation(models.Model):
    """
    树形结构关系
    """

    class Meta:
        verbose_name = "树形结构关系"
        db_table = "relation"

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, db_constraint=False
    )
    tree = models.TextField("结构主题", null=False, default=[])
    type = models.IntegerField("树类型", default=1)


class Visit(models.Model):
    METHODS = Choices(
        ("GET", "GET"),
        ("POST", "POST"),
        ("PUT", "PUT"),
        ("PATCH", "PATCH"),
        ("DELETE", "DELETE"),
        ("OPTION", "OPTION"),
    )

    user = models.CharField(
        max_length=100, verbose_name="访问url的用户名", db_index=True
    )
    ip = models.CharField(
        max_length=20, verbose_name="用户的ip", db_index=True
    )
    project = models.CharField(
        max_length=4, verbose_name="项目id", db_index=True, default=0
    )
    url = models.CharField(
        max_length=255, verbose_name="被访问的url", db_index=True
    )
    path = models.CharField(
        max_length=100,
        verbose_name="被访问的接口路径",
        default="",
        db_index=True,
    )
    request_params = models.CharField(
        max_length=255, verbose_name="请求参数", default="", db_index=True
    )
    request_method = models.CharField(
        max_length=7, verbose_name="请求方法", choices=METHODS, db_index=True
    )
    request_body = models.TextField(verbose_name="请求体")
    create_time = models.DateTimeField(
        "创建时间", auto_now_add=True, db_index=True
    )

    class Meta:
        db_table = "visit"
