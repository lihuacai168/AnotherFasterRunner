import json

import time

from crontab import CronTab
from django.db.models import Q
from rest_framework import serializers
from fastrunner import models
from fastrunner.utils.parser import Parse
from djcelery import models as celery_models

from fastrunner.utils.tree import get_tree_relation_name


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目信息序列化
    """

    api_cover_rate = serializers.SerializerMethodField()

    class Meta:
        model = models.Project
        fields = ['id', 'name', 'desc', 'responsible', 'update_time', 'creator', 'updater', 'yapi_openapi_token', 'yapi_base_url', 'api_cover_rate']

    def get_api_cover_rate(self, obj):
        """
        接口覆盖率，百分比后去两位小数点
        """
        apis = models.API.objects.filter(project_id=obj.id).values('url', 'method')
        api_unique = {f'{api["url"]}_{api["method"]}' for api in apis}
        case_steps = models.CaseStep.objects.filter(case__project_id=obj.id).filter(~Q(method='config')).values('url', 'method')
        case_steps_unique = {f'{case_step["url"]}_{case_step["method"]}' for case_step in case_steps}
        if len(api_unique) == 0:
            return '0.00'
        if len(case_steps_unique) > len(api_unique):
            return '100.00'
        return '%.2f' % (len(case_steps_unique & api_unique) / len(api_unique) * 100)


class VisitSerializer(serializers.ModelSerializer):
    """
    访问统计序列化
    """

    class Meta:
        model = models.Visit
        fields = '__all__'


class DebugTalkSerializer(serializers.ModelSerializer):
    """
    驱动代码序列化
    """

    class Meta:
        model = models.Debugtalk
        # fields = ['id', 'code', 'creator', 'updater']
        fields = '__all__'


class RelationSerializer(serializers.ModelSerializer):
    """
    树形结构序列化
    """

    class Meta:
        model = models.Relation
        fields = '__all__'


class AssertSerializer(serializers.Serializer):
    class Meta:
        models = models.API

    node = serializers.IntegerField(min_value=0, default='')
    # max_value=models.Project.objects.latest('id').id 会导致数据库迁移找不到project
    project = serializers.IntegerField(required=True, min_value=1)
    search = serializers.CharField(default='')
    tag = serializers.ChoiceField(choices=models.API.TAG, default='')
    rigEnv = serializers.ChoiceField(choices=models.API.ENV_TYPE, default='')
    delete = serializers.ChoiceField(choices=(0, 1), default=0)
    onlyMe = serializers.BooleanField(default=False)


# 用例反序列化验证器
class CaseSearchSerializer(serializers.Serializer):
    node = serializers.IntegerField(min_value=0, default='')
    project = serializers.IntegerField(required=True, min_value=1)
    search = serializers.CharField(default='')
    searchType = serializers.CharField(default='')
    caseType = serializers.CharField(default='')
    onlyMe = serializers.BooleanField(default=False)


class CaseSerializer(serializers.ModelSerializer):
    """
    用例信息序列化
    """
    tag = serializers.CharField(source="get_tag_display")

    class Meta:
        model = models.Case
        fields = '__all__'


class CaseStepSerializer(serializers.ModelSerializer):
    """
    用例步骤序列化
    """
    body = serializers.SerializerMethodField()

    class Meta:
        model = models.CaseStep
        fields = ['id', 'name', 'url', 'method', 'body', 'case', 'source_api_id', 'creator', 'updater']
        depth = 1

    def get_body(self, obj):
        body = eval(obj.body)
        if "base_url" in body["request"].keys():
            return {
                "name": body["name"],
                "method": "config"
            }
        else:
            parse = Parse(eval(obj.body))
            parse.parse_http()
            return parse.testcase


class APIRelatedCaseSerializer(serializers.Serializer):
    case_name = serializers.CharField(source='case.name')
    case_id = serializers.CharField(source='case.id')

    class Meta:
        fields = ['case_id', 'case_name']


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
        fields = ['id', 'name', 'url', 'method', 'project', 'relation', 'body', 'rig_env', 'tag', 'tag_name',
                  'update_time', 'delete', 'creator', 'updater', 'cases', 'relation_name']

    def get_body(self, obj):
        parse = Parse(eval(obj.body))
        parse.parse_http()
        return parse.testcase

    def get_cases(self, obj):
        cases = models.CaseStep.objects.filter(source_api_id=obj.id)
        case_id = APIRelatedCaseSerializer(many=True, instance=cases)
        return case_id.data

    def get_relation_name(self, obj):
        relation_obj = models.Relation.objects.get(project_id=obj.project_id, type=1)
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
        fields = ['id', 'base_url', 'body', 'name', 'update_time', 'is_default', 'creator', 'updater']
        depth = 1

    def get_body(self, obj):
        parse = Parse(eval(obj.body), level='config')
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

    class Meta:
        model = models.Report
        fields = ["id", "name", "type", "time", "stat", "platform", "success", 'creator', 'updater']

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
    key = serializers.CharField(allow_null=False, max_length=100, required=True)
    value = serializers.CharField(allow_null=False, max_length=1024)
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = models.Variables
        fields = '__all__'


class HostIPSerializer(serializers.ModelSerializer):
    """
    变量信息序列化
    """

    class Meta:
        model = models.HostIP
        fields = '__all__'


def get_cron_next_execute_time(crontab_expr: str):
    entry = CronTab(crontab_expr)
    return int(entry.next(default_utc=False)+time.time())


class PeriodicTaskSerializer(serializers.ModelSerializer):
    """
    定时任务信列表序列化
    """
    kwargs = serializers.SerializerMethodField()
    args = serializers.SerializerMethodField()

    class Meta:
        model = celery_models.PeriodicTask
        fields = ['id', 'name', 'args', 'kwargs', 'enabled', 'date_changed', 'enabled', 'description']

    def get_kwargs(self, obj):
        kwargs = json.loads(obj.kwargs)
        if obj.enabled:
            kwargs['next_execute_time'] = get_cron_next_execute_time(kwargs['crontab'])
        return kwargs

    def get_args(self, obj):
        case_id_list = json.loads(obj.args)
        # 数据格式,list of dict : [{"id":case_id,"name":case_name}]
        return list(models.Case.objects.filter(pk__in=case_id_list).values('id', 'name'))
