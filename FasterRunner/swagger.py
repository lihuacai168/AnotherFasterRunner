# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: swagger.py
# @Time : 2020/12/28 22:04
# @Email: lihuacai168@gmail.com

from drf_yasg.inspectors import SwaggerAutoSchema


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        tags = super().get_tags(operation_keys)

        if "api" in tags and operation_keys:
            #  `operation_keys` 内容像这样 ['v1', 'prize_join_log', 'create']
            tags[0] = operation_keys[2]

        return tags
