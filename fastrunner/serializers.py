import json

from rest_framework import serializers
from fastrunner import models
from fastrunner.utils.parser import Parse
from djcelery import models as celery_models


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目信息序列化
    """

    class Meta:
        model = models.Project
        fields = ['id', 'name', 'desc', 'responsible', 'update_time']


class DebugTalkSerializer(serializers.ModelSerializer):
    """
    驱动代码序列化
    """

    class Meta:
        model = models.Debugtalk
        fields = ['id', 'code']


class RelationSerializer(serializers.ModelSerializer):
    """
    树形结构序列化
    """

    class Meta:
        model = models.Relation
        fields = '__all__'


class APISerializer(serializers.ModelSerializer):
    """
    接口信息序列化
    """
    body = serializers.SerializerMethodField()
    # tag = serializers.CharField(source="get_tag_display")
    tag_name = serializers.CharField(source="get_tag_display")
    class Meta:
        model = models.API
        fields = ['id', 'name', 'url', 'method', 'project', 'relation', 'body', 'rig_env', 'tag', 'tag_name']

    def get_body(self, obj):
        parse = Parse(eval(obj.body))
        parse.parse_http()
        return parse.testcase


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
        fields = ['id', 'name', 'url', 'method', 'body', 'case']
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


class ConfigSerializer(serializers.ModelSerializer):
    """
    配置信息序列化
    """
    body = serializers.SerializerMethodField()

    class Meta:
        model = models.Config
        fields = ['id', 'base_url', 'body', 'name', 'update_time', 'is_default']
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
        fields = ["id", "name", "type", "time", "stat", "platform", "success"]

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
        return json.loads(obj.kwargs)

    def get_args(self, obj):
        case_id_list = json.loads(obj.args)
        # 数据格式,list of dict : [{"id":case_id,"name":case_name}]
        return list(models.Case.objects.filter(pk__in=case_id_list).values('id', 'name'))
