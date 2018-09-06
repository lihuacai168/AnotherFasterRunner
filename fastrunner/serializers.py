from rest_framework import serializers
from fastrunner import models


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
        fields = ['id', 'debugtalk']


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

    class Meta:
        model = models.API
        fields = ['id', 'name', 'url', 'method', 'update_time', 'project', 'relation']
