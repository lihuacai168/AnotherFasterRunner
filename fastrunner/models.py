from django.db import models

# Create your models here.
from usermanager.models import BaseTable


class LocustDetail(BaseTable):
    """
    压测信息表
    """

    class Meta:
        verbose_name = "压测信息"
        db_table = "LocustDetail"

    suite_id = models.IntegerField('自动化测试用例集ID', unique=True, null=False)
    suite_name = models.CharField('用例集名称', max_length=100)
    config_id = models.IntegerField('配置ID')
    config_name = models.CharField('配置名称', max_length=100)
    config_url = models.CharField('配置地址', max_length=100)
    port = models.IntegerField('端口')
    project = models.IntegerField('项目id')
    task = models.CharField('pid合集', max_length=100)


class Project(BaseTable):
    """
    项目信息表
    """

    class Meta:
        verbose_name = "项目信息"
        db_table = "Project"

    name = models.CharField("项目名称", unique=True, null=False, max_length=50)
    desc = models.CharField("简要介绍", max_length=100, null=False)
    responsible = models.CharField("创建人", max_length=20, null=False)


class Team(BaseTable):
    """
    项目成员
    """

    permission_union = (
        (1, "admin"),
        (2, "read"),
        (3, "write"),
        (4, "delete"),
        (5, "admin")
    )

    class Meta:
        verbose_name = "项目成员"
        db_table = "Team"

    account = models.CharField("账号", max_length=20)
    permission = models.IntegerField("权限", choices=permission_union)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Debugtalk(models.Model):
    """
    驱动文件表
    """

    class Meta:
        verbose_name = "驱动库"
        db_table = "Debugtalk"

    code = models.TextField("python代码", default="# write you code", null=False)
    project = models.OneToOneField(to=Project, on_delete=models.CASCADE)


class Config(BaseTable):
    """
    环境信息表
    """

    class Meta:
        verbose_name = "环境信息"
        db_table = "Config"

    name = models.CharField("环境名称", null=False, max_length=50)
    body = models.TextField("主体信息", null=False)
    base_url = models.CharField("请求地址", null=False, max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class API(BaseTable):
    """
    API信息表
    """

    class Meta:
        verbose_name = "接口信息"
        db_table = "API"

    name = models.CharField("接口名称", null=False, max_length=50)
    body = models.TextField("主体信息", null=False)
    url = models.CharField("请求地址", null=False, max_length=2000)
    method = models.CharField("请求方式", null=False, max_length=10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    relation = models.IntegerField("节点id", null=False)


class Case(BaseTable):
    """
    用例信息表
    """

    class Meta:
        verbose_name = "用例信息"
        db_table = "Case"

    name = models.CharField("用例名称", null=False, max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    relation = models.IntegerField("节点id", null=False)


class CaseStep(BaseTable):
    """
    Test Case Step
    """

    class Meta:
        verbose_name = "用例信息 Step"
        db_table = "CaseStep"

    name = models.CharField("用例名称", null=False, max_length=50)
    body = models.TextField("主体信息", null=False)
    url = models.CharField("请求地址", null=False, max_length=100)
    method = models.CharField("请求方式", null=False, max_length=10)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    step = models.IntegerField("顺序", null=False)


class DataBase(BaseTable):
    """
    数据库信息表
    """

    db_type = (
        (1, "Sql Server"),
        (2, "MySQL"),
        (3, "Oracle"),
        (4, "Mongodb"),
        (5, "InfluxDB")
    )

    class Meta:
        verbose_name = "数据库信息"
        db_table = "DataBase"

    name = models.CharField("数据库名称", null=False, max_length=50)
    server = models.CharField("服务地址", null=False, max_length=100)
    account = models.CharField("登录名", max_length=50, null=False)
    password = models.CharField("登陆密码", max_length=50, null=False)
    type = models.IntegerField('数据库类型', default=2, choices=db_type)
    desc = models.CharField("描述", max_length=50, null=False)


class FileBinary(models.Model):
    """
    二进制文件流
    """

    class Meta:
        verbose_name = "二进制文件"
        db_table = "FileBinary"

    name = models.CharField("文件名称", unique=True, null=False, max_length=50)
    body = models.BinaryField("二进制流", null=False)
    size = models.CharField("大小", null=False, max_length=30)


class ReportRelation(BaseTable):
    report_type = (
        (1, "api"),
        (2, "test_set"),
        (3, "schedule"),
        (4, "CI")
    )
    result_status = (
        ("N/A", "N/A"),
        ("success", "success"),
        ("failure", "failure")
    )

    class Meta:
        verbose_name = "测试报告来源关系"
        db_table = "ReportRelation"

    name = models.CharField("测试报告名称", null=False, max_length=50)
    ref = models.IntegerField("测试报告来源", null=False, choices=report_type, default=1)
    project = models.IntegerField("项目id", null=False, default=0)
    status = models.CharField("状态", max_length=30, null=False, choices=result_status, default="N/A")


class Report(BaseTable):
    class Meta:
        verbose_name = "测试报告"
        db_table = "Report"

    refId = models.IntegerField("报告Id", null=False, default=0)
    reportRelation = models.ForeignKey(ReportRelation, default=1, verbose_name='报告依赖id', related_name='reports',
                                       on_delete=models.CASCADE)
    content = models.TextField("报告内容")


class Relation(models.Model):
    """
    树形结构关系
    """

    class Meta:
        verbose_name = "树形结构关系"
        db_table = "Relation"

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tree = models.TextField("结构主题", null=False, default=[])
    type = models.IntegerField("树类型", default=1)
