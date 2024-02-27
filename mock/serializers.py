# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: serializers.py
# @Time : 2024/2/25 18:59
# @Email: lihuacai168@gmail.com

from rest_framework import serializers

from .models import MockAPI, MockProject


class MockAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = MockAPI
        fields = ["project", "request_path", "request_method", "response_text", "is_active"]


class MockProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockProject
        fields = ["project_id", "project_name", "project_desc", "is_active"]
