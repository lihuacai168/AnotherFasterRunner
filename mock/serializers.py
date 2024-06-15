# !/usr/bin/python3
# -*- coding: utf-8 -*-
import ast

# @Author: 花菜
# @File: serializers.py
# @Time : 2024/2/25 18:59
# @Email: lihuacai168@gmail.com

from rest_framework import serializers

from .models import MockAPI, MockProject, MockAPILog


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
            "version",
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
        extra_kwargs = {
            'project': {'required': True},
            'request_path': {'required': True},
            'response_text': {'required': True},
        }

    def validate_response_text(self, value):
        """
        Custom validation for 'response_text' to ensure it's valid Python code
        and contains the 'execute' function.
        """
        if value is None:
            raise serializers.ValidationError("response_text必须提供")
        try:
            tree = ast.parse(value)
        except SyntaxError as e:
            raise serializers.ValidationError(f"python语法错误: {e}")

        # 检查是否包含execute函数
        execute_function_exists = any(
            isinstance(node, ast.FunctionDef) and node.name == 'execute'
            for node in ast.walk(tree)
        )

        if not execute_function_exists:
            raise serializers.ValidationError("缺少必要的函数：`def execute(req, resp): ...`")

        # 额外的函数定义错误检查
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == 'execute':
                # 检查execute函数的参数
                args = node.args
                if len(args.args) != 2 or args.args[0].arg != 'req' or args.args[1].arg != 'resp':
                    raise serializers.ValidationError(
                        "`execute`函数必须包含两个参数：`req`和`resp`。"
                    )

        return value

    def validate_project(self, obj):
        """
        自定义校验project
        """
        if obj is None:
            raise serializers.ValidationError("项目必须提供")

        if not MockProject.objects.filter(project_id=obj.project_id).exists():
            raise serializers.ValidationError(f"项目`{obj.project_id}`不存在")
        return obj


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


class MockAPILogSerializer(serializers.ModelSerializer):
    api = serializers.PrimaryKeyRelatedField(queryset=MockAPI.objects.all())
    project = serializers.PrimaryKeyRelatedField(queryset=MockProject.objects.all())

    class Meta:
        model = MockAPILog
        fields = '__all__'
