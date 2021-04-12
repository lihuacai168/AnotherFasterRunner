# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: yapi.py
# @Time : 2021/3/31 22:56
# @Email: lihuacai168@gmail.com
from loguru import logger
from rest_framework.views import APIView
from rest_framework.response import Response
from django_bulk_update.helper import bulk_update

from fastrunner.utils.parser import Yapi
from fastrunner.utils import response
from fastrunner import models


class YAPIView(APIView):

    def post(self, request, **kwargs):
        faster_project_id = kwargs['pk']
        obj = models.Project.objects.get(pk=faster_project_id)
        token = obj.yapi_openapi_token
        yapi_base_url = obj.yapi_base_url
        yapi = Yapi(yapi_base_url=yapi_base_url, token=token, faster_project_id=faster_project_id)

        try:
            # 获取yapi的分组，然后更新api tree
            yapi.create_relation_id(yapi.fast_project_id)

            # 获取yapi所有的api的id
            yapi.get_api_ids()

            # 通过id获取所有api的详情
            yapi.get_api_info()
        except Exception as e:
            logger.error(f'导入yapi失败： {e}')
            return Response(response.YAPI_ADD_FAILED)

        # 把yapi解析成符合faster的api格式
        parsed_apis: list = yapi.get_parsed_apis()
        imported_apis = models.API.objects.filter(project_id=faster_project_id, creator='yapi')
        update_apis, new_apis = yapi.merge_api(parsed_apis, imported_apis)
        created_objs = models.API.objects.bulk_create(objs=new_apis)
        bulk_update(update_apis)

        parsed_apis_count = len(parsed_apis)
        created_apis_count = len(created_objs)
        updated_apis_count = len(update_apis)
        resp = {"获取api个数": parsed_apis_count,
                "新增导入api个数": created_apis_count,
                "更新api个数": updated_apis_count,
        }
        resp.update(response.YAPI_ADD_SUCCESS)
        return Response(resp)