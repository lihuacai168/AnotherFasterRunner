# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: serializers.py
# @Time : 2024/2/25 18:59
# @Email: lihuacai168@gmail.com

from rest_framework import serializers

from .models import MockAPI, MockProject


class MockAPISerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.project_name", read_only=True)

    class Meta:
        model = MockAPI
        fields = [
            "id",
            "project",
            "project_name",
            "request_path",
            "request_method",
            "request_body",
            "response_text",
            "is_active",
            "api_id",
            "api_desc",
            "api_name",
            "creator",
            "updater",
            "create_time",
            "update_time",
        ]
        read_only_fields = [
            "id",
            "api_id",
            "creator",
            "updater",
            "create_time",
            "update_time",
        ]


class MockProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockProject
        fields = [
            "id",
            "project_id",
            "project_name",
            "project_desc",
            "is_active",
            "creator",
            "updater",
            "create_time",
            "update_time",
        ]
        read_only_fields = ["id", "creator", "updater", "create_time", "update_time", "project_id"]
