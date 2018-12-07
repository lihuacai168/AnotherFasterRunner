import simplejson
from rest_framework import serializers
from extends import models as etModels
from fastrunner import models
from fastrunner.utils.parser import Parse


class ScheduleReporterSerializer(serializers.ModelSerializer):
    scheduleId = serializers.CharField(required=False)
    """
    定时任务发送人员序列化
    """

    class Meta:
        model = etModels.ScheduleReporter
        fields = ['id', 'userId', 'userName', 'email', 'scheduleId']


class ScheduleDetailsSerializer(serializers.ModelSerializer):
    scheduleId = serializers.CharField(required=False)
    """
    定时任务发送人员序列化
    """

    class Meta:
        model = etModels.ScheduleDetail
        fields = ['id', 'scheduleId', 'stepId', 'stepRef', 'stepName', 'configId']


class ScheduleSerializer(serializers.ModelSerializer):
    """
    定时任务序列化
    """
    reporters = ScheduleReporterSerializer(many=True)
    details = ScheduleDetailsSerializer(many=True)
    update_time = serializers.DateTimeField(required=False)

    class Meta:
        model = etModels.Schedule
        fields = ['id', 'name', 'desc', 'responsible', 'update_time', 'cron', 'project', 'reporters', 'details',
                  'sendType']

    def create(self, validated_data):
        reporters = validated_data.pop('reporters')
        details = validated_data.pop('details')
        schedule_id = etModels.Schedule.objects.create(**validated_data)
        for report in reporters:
            etModels.ScheduleReporter.objects.create(scheduleId=schedule_id, **report)
        for detail in details:
            etModels.ScheduleDetail.objects.create(scheduleId=schedule_id, **detail)
        return schedule_id


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


class ConfigListSerializer(serializers.ModelSerializer):
    """
    配置信息序列化
    """

    class Meta:
        model = models.Config
        fields = ['id', 'base_url', 'name']


class ReportSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()

    class Meta:
        model = models.Report
        fields = ['id', 'refId', 'content', 'detail']

    def get_content(self, obj):
        return simplejson.loads(obj.content, encoding="UTF-8")

    def get_detail(self, obj):
        refId = obj.refId
        data = {}
        try:
            data = ScheduleDetailsSerializer(etModels.ScheduleDetail.objects.get(pk=refId)).data
        except Exception:
            pass
        return data


class ReportRelationSerializer(serializers.ModelSerializer):
    reports = ReportSerializer(many=True)

    class Meta:
        model = models.ReportRelation
        fields = '__all__'

    def create(self, validated_data):
        projectReports = validated_data.pop('reports')
        reportRelation_id = models.ReportRelation.objects.create(**validated_data)
        for report in projectReports:
            models.Report.objects.create(reportRelation=reportRelation_id, **report)
