# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: log_record_serializer.py
# @Time : 2023/9/17 22:55
# @Email: lihuacai168@gmail.com

from rest_framework import serializers
from system.models import LogRecord


class LogRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogRecord
        fields = "__all__"
