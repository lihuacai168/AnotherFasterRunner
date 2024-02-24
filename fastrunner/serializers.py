import json
import logging
from typing import Union
import datetime


import croniter
from django.db.models import Q
from django_celery_beat.models import PeriodicTask

from rest_framework import serializers
from fastrunner import models
from fastrunner.utils.parser import Parse

from fastrunner.utils.tree import get_tree_relation_name

logger = logging.getLogger(__name__)


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目信息序列化
    """

    api_cover_rate = serializers.SerializerMethodField()

    class Meta:
        model = models.Project
        fields = [
            "id",
            "name",
            "desc",
            "responsible",
            "update_time",
            "creator",
            "updater",
            "yapi_openapi_token",
            "yapi_base_url",
            "api_cover_rate",
            "jira_project_key",
            "jira_bearer_token",
        ]

    def get_api_cover_rate(self, obj):
        """
        接口覆盖率，百分比后去两位小数点
        """
        apis = (
            models.API.objects.filter(project_id=obj.id, delete=0)
            .filter(~Q(tag=4))
            .values("url", "method")
        )
        api_unique = {f'{api["url"]}_{api["method"]}' for api in apis}
        case_steps = (
            models.CaseStep.objects.filter(case__project_id=obj.id)
            .filter(~Q(method="config"))
            .values("url", "method")
        )
        case_steps_unique = {
            f'{case_step["url"]}_{case_step["method"]}'
            for case_step in case_steps
        }
        if len(api_unique) == 0:
            return "0.00"
        if len(case_steps_unique) > len(api_unique):
            return "100.00"
        return "%.2f" % (
            len(case_steps_unique & api_unique) / len(api_unique) * 100
        )


class VisitSerializer(serializers.ModelSerializer):
    """
    访问统计序列化
    """

    class Meta:
        model = models.Visit
        fields = "__all__"


class DebugTalkSerializer(serializers.ModelSerializer):
    """
    驱动代码序列化
    """

    class Meta:
        model = models.Debugtalk
        # fields = ['id', 'code', 'creator', 'updater']
        fields = "__all__"


class RelationSerializer(serializers.ModelSerializer):
    """
    树形结构序列化
    """

    class Meta:
        model = models.Relation
        fields = "__all__"


class AssertSerializer(serializers.Serializer):
    class Meta:
        models = models.API

    node = serializers.IntegerField(min_value=0, default="")
    # max_value=models.Project.objects.latest('id').id 会导致数据库迁移找不到project
    project = serializers.IntegerField(required=True, min_value=1)
    search = serializers.CharField(default="")
    creator = serializers.CharField(required=False, default="")
    tag = serializers.ChoiceField(choices=models.API.TAG, default="")
    rigEnv = serializers.ChoiceField(choices=models.API.ENV_TYPE, default="")
    delete = serializers.ChoiceField(choices=(0, 1), default=0)
    onlyMe = serializers.BooleanField(default=False)
    showYAPI = serializers.BooleanField(default=True)


# 用例反序列化验证器
class CaseSearchSerializer(serializers.Serializer):
    node = serializers.IntegerField(min_value=0, default="")
    project = serializers.IntegerField(required=True, min_value=1)
    search = serializers.CharField(default="")
    searchType = serializers.CharField(default="")
    caseType = serializers.CharField(default="")
    onlyMe = serializers.BooleanField(default=False)


class CaseSerializer(serializers.ModelSerializer):
    """
    用例信息序列化
    """

    tag = serializers.CharField(source="get_tag_display")
    tasks = serializers.ListField(read_only=True)  # 包含用例的定时任务

    class Meta:
        model = models.Case
        fields = "__all__"


class CaseStepSerializer(serializers.ModelSerializer):
    """
    用例步骤序列化
    """

    body = serializers.SerializerMethodField()

    class Meta:
        model = models.CaseStep
        fields = [
            "id",
            "name",
            "url",
            "method",
            "body",
            "case",
            "source_api_id",
            "creator",
            "updater",
        ]
        depth = 1

    def get_body(self, obj):
        body = eval(obj.body)
        if "base_url" in body["request"].keys():
            return {"name": body["name"], "method": "config"}
        else:
            parse = Parse(eval(obj.body))
            parse.parse_http()
            return parse.testcase


class CIReportSerializer(serializers.Serializer):
    ci_job_id = serializers.IntegerField(
        required=True, min_value=1, help_text="gitlab-ci job id"
    )


class CISerializer(serializers.Serializer):
    # project = serializers.IntegerField(
    #     required=True, min_value=1, help_text='测试平台中某个项目的id')
    # task_ids = serializers.CharField(required=True, max_length=200, allow_blank=True)
    ci_job_id = serializers.IntegerField(
        required=True, min_value=1, help_text="gitlab-ci job id"
    )
    ci_job_url = serializers.CharField(required=True, max_length=500)
    ci_pipeline_id = serializers.IntegerField(required=True)
    ci_pipeline_url = serializers.CharField(required=True, max_length=500)
    ci_project_id = serializers.IntegerField(required=True, min_value=1)
    ci_project_name = serializers.CharField(required=True, max_length=100)
    ci_project_namespace = serializers.CharField(required=True, max_length=100)
    env = serializers.CharField(required=False, max_length=100)
    start_job_user = serializers.CharField(
        required=True, max_length=100, help_text="GITLAB_USER_NAME"
    )


class APIRelatedCaseSerializer(serializers.Serializer):
    case_name = serializers.CharField(source="case.name")
    case_id = serializers.CharField(source="case.id")

    class Meta:
        fields = ["case_id", "case_name"]


class APISerializer(serializers.ModelSerializer):
    """
    接口信息序列化
    """

    body = serializers.SerializerMethodField()
    tag_name = serializers.CharField(source="get_tag_display")
    cases = serializers.SerializerMethodField()
    relation_name = serializers.SerializerMethodField()

    class Meta:
        model = models.API
        # fields = '__all__'
        fields = [
            "id",
            "name",
            "url",
            "method",
            "project",
            "relation",
            "body",
            "rig_env",
            "tag",
            "tag_name",
            "update_time",
            "delete",
            "creator",
            "updater",
            "cases",
            "relation_name",
        ]

    def get_body(self, obj):
        parse = Parse(eval(obj.body))
        parse.parse_http()
        return parse.testcase

    def get_cases(self, obj):
        cases = models.CaseStep.objects.filter(source_api_id=obj.id)
        case_id = APIRelatedCaseSerializer(many=True, instance=cases)
        return case_id.data

    def get_relation_name(self, obj):
        relation_obj = models.Relation.objects.get(
            project_id=obj.project_id, type=1
        )
        label = get_tree_relation_name(eval(relation_obj.tree), obj.relation)
        return label

    # def get_cases(self, obj):
    #     cases = obj.api_case_relate.all()
    #     case_id = CaseSerializer(many=True, instance=cases)
    #     return case_id.data


class ConfigSerializer(serializers.ModelSerializer):
    """
    配置信息序列化
    """

    body = serializers.SerializerMethodField()

    class Meta:
        model = models.Config
        fields = [
            "id",
            "base_url",
            "body",
            "name",
            "update_time",
            "is_default",
            "creator",
            "updater",
        ]
        depth = 1

    def get_body(self, obj):
        parse = Parse(eval(obj.body), level="config")
        parse.parse_http()
        return parse.testcase


class ReportSerializer(serializers.ModelSerializer):
    """
    报告信息序列化
    """

    type = serializers.CharField(source="get_type_display")
    time = serializers.SerializerMethodField()
    stat = serializers.SerializerMethodField()
    platform = serializers.SerializerMethodField()
    success = serializers.SerializerMethodField()
    ci_job_url = serializers.CharField()

    class Meta:
        model = models.Report
        fields = [
            "id",
            "name",
            "type",
            "time",
            "stat",
            "platform",
            "success",
            "creator",
            "updater",
            "ci_job_url",
        ]

    def get_time(self, obj):
        return json.loads(obj.summary)["time"]

    def get_stat(self, obj):
        return json.loads(obj.summary)["stat"]

    def get_platform(self, obj):
        return json.loads(obj.summary)["platform"]

    def get_success(self, obj):
        return json.loads(obj.summary)["success"]


class VariablesSerializer(serializers.ModelSerializer):
    """
    变量信息序列化
    """

    key = serializers.CharField(
        allow_null=False, max_length=100, required=True
    )
    value = serializers.CharField(allow_null=False, max_length=1024)
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = models.Variables
        fields = "__all__"


class HostIPSerializer(serializers.ModelSerializer):
    """
    变量信息序列化
    """

    class Meta:
        model = models.HostIP
        fields = "__all__"


def get_cron_next_execute_time(crontab_expr: str) -> int:
    now = datetime.datetime.now()
    try:
        cron = croniter.croniter(crontab_expr, now)
    except croniter.CroniterNotAlphaError:
        logger.warning(f"解析定时任务{crontab_expr=} 错误，返回0")
        # 解析定时任务错误，返回0
        return 0

    next_time: datetime.datetime = cron.get_next(datetime.datetime)
    return int(next_time.timestamp())


class PeriodicTaskSerializer(serializers.ModelSerializer):
    """
    定时任务信列表序列化
    """

    kwargs = serializers.SerializerMethodField()
    args = serializers.SerializerMethodField()
    last_run_at = serializers.SerializerMethodField()

    class Meta:
        model = PeriodicTask
        fields = [
            "id",
            "name",
            "args",
            "kwargs",
            "enabled",
            "date_changed",
            "enabled",
            "description",
            "total_run_count",
            "last_run_at",
        ]

    def get_kwargs(self, obj):
        kwargs = json.loads(obj.kwargs)
        if obj.enabled:
            kwargs["next_execute_time"] = get_cron_next_execute_time(
                kwargs["crontab"]
            )
        # ci_project_ids = eval(kwargs.get('ci_project_ids', '[]'))
        # kwargs['ci_project_ids'] = ','.join(map(lambda x: str(x), ci_project_ids))
        kwargs["ci_project_ids"] = kwargs.get("ci_project_ids", "")
        kwargs["ci_env"] = kwargs.get("ci_env", "请选择")
        kwargs["config"] = kwargs.get("config", "请选择")
        # False:串行, True:并行
        kwargs["is_parallel"] = kwargs.get("is_parallel", False)
        return kwargs

    def get_args(self, obj):
        case_id_list = json.loads(obj.args)
        # 数据格式,list of dict : [{"id":case_id,"name":case_name}]
        return list(
            models.Case.objects.filter(pk__in=case_id_list).values(
                "id", "name"
            )
        )

    def get_last_run_at(self, obj) -> Union[str, int]:
        if obj.last_run_at:
            return int(obj.last_run_at.timestamp())
        return ""


class ScheduleDeSerializer(serializers.Serializer):
    """
    定时任务反序列
    """

    switch = serializers.BooleanField(required=True, help_text="定时任务开关")
    crontab = serializers.CharField(
        required=True,
        help_text="定时任务表达式",
        max_length=100,
        allow_blank=True,
    )
    ci_project_ids = serializers.CharField(
        required=True,
        allow_blank=True,
        help_text="Gitlab的项目id，多个用逗号分开，一个项目id对应多个task，但只能在同一个项目中",
    )
    strategy = serializers.CharField(
        required=True, help_text="发送通知策略", max_length=20
    )
    receiver = serializers.CharField(
        required=True,
        help_text="邮件接收者，暂时用不上",
        allow_blank=True,
        max_length=100,
    )
    mail_cc = serializers.CharField(
        required=True,
        help_text="邮件抄送列表，暂时用不上",
        allow_blank=True,
        max_length=100,
    )
    name = serializers.CharField(
        required=True, help_text="定时任务的名字", max_length=100
    )
    webhook = serializers.CharField(
        required=True,
        help_text="飞书webhook url",
        trim_whitespace=True,
        allow_blank=True,
        max_length=500,
    )
    updater = serializers.CharField(
        required=False,
        help_text="更新人",
        max_length=20,
        allow_null=True,
        allow_blank=True,
    )
    creator = serializers.CharField(
        required=False,
        help_text="创建人",
        max_length=20,
        allow_null=True,
        allow_blank=True,
    )
    data = serializers.ListField(required=True, help_text="用例id")
    project = serializers.IntegerField(
        required=True, help_text="测试平台的项目id", min_value=1
    )

    def validate_ci_project_ids(self, ci_project_ids):
        if ci_project_ids:
            not_allowed_project_ids = set()
            kwargs_list = PeriodicTask.objects.filter(
                ~Q(description=self.initial_data["project"])
            ).values("kwargs")
            for kwargs in kwargs_list:
                not_allowed_project_id: str = json.loads(kwargs["kwargs"]).get(
                    "ci_project_ids", ""
                )
                if not_allowed_project_id:
                    not_allowed_project_ids.update(
                        not_allowed_project_id.split(",")
                    )

            validation_errors = set()
            for ci_project_id in ci_project_ids.split(","):
                if ci_project_id in not_allowed_project_ids:
                    validation_errors.add(ci_project_id)

            if validation_errors:
                raise serializers.ValidationError(
                    f"{','.join(validation_errors)} 已经在其他项目存在"
                )
