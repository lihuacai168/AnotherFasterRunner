import json

from rest_framework import serializers
from fastrunner import models
from fastrunner.utils.parser import Parse


class ProjectSerializer(serializers.ModelSerializer):
    """
    项目信息序列化
    """

    class Meta:
        model = models.Project
        fields = ['id', 'name', 'desc', 'responsible', 'update_time']


class TeamSerializer(serializers.ModelSerializer):
    """
    项目成员序列化
    """
    permission = serializers.CharField(source="get_permission_display")
    project = serializers.CharField(source="project.name")

    class Meta:
        model = models.Team
        fields = ["id", "account", "permission", "project"]


class DataBaseSerializer(serializers.ModelSerializer):
    """
    数据库信息序列化
    """

    # type = serializers.CharField(source="get_type_display")

    class Meta:
        model = models.DataBase
        fields = '__all__'


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

    class Meta:
        model = models.API
        fields = ['id', 'name', 'url', 'method', 'project', 'relation', 'body']

    def get_body(self, obj):
        parse = Parse(eval(obj.body))
        parse.parse_http()
        return parse.testcase


class CaseSerializer(serializers.ModelSerializer):
    """
    用例信息序列化
    """

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
        fields = ['id', 'base_url', 'body', 'name', 'update_time']
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
    project = serializers.CharField(source="project.name")
    summary = serializers.SerializerMethodField()

    class Meta:
        model = models.Report
        fields = ["id", "name", "type", "project", "summary"]

    def get_summary(self, obj):
        return json.loads(obj.summary)


class VariablesSerializer(serializers.ModelSerializer):
    """
    变量信息序列化
    """

    class Meta:
        model = models.Variables
        fields = '__all__'
