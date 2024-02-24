# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: yapi.py
# @Time : 2021/3/31 22:56
# @Email: lihuacai168@gmail.com
# from loguru import logger
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from django_bulk_update.helper import bulk_update

from fastrunner.utils.parser import Yapi
from fastrunner.utils import response
from fastrunner import models

logger = logging.getLogger(__name__)


class YAPIView(APIView):

    def post(self, request, **kwargs):
        logger.info("开始批量导入yapi接口...")
        faster_project_id = kwargs['pk']
        obj = models.Project.objects.get(pk=faster_project_id)
        token = obj.yapi_openapi_token
        yapi_base_url = obj.yapi_base_url
        yapi = Yapi(yapi_base_url=yapi_base_url, token=token, faster_project_id=faster_project_id)
        imported_apis = models.API.objects.filter(project_id=faster_project_id, creator='yapi', delete=0)
        imported_apis_mapping = {api.yapi_id: api.ypai_up_time for api in imported_apis}
        create_ids, update_ids = yapi.get_create_or_update_apis(imported_apis_mapping)
        try:
            # 获取yapi的分组，然后更新api tree
            yapi.create_relation_id(yapi.fast_project_id)

            # 通过id获取所有api的详情
            create_ids.extend(update_ids)
            if len(create_ids) == 0:
                logger.info("yapi没有需要导入到平台的接口...")
                return Response(response.YAPI_NOT_NEED_CREATE_OR_UPDATE)
            api_info = yapi.get_batch_api_detail(create_ids)
        except Exception as e:
            logger.error(f'导入yapi失败： {e}')
            return Response(response.YAPI_ADD_FAILED)

        # 把yapi解析成符合faster的api格式
        parsed_apis: list = yapi.get_parsed_apis(api_info)
        update_apis, new_apis = yapi.merge_api(parsed_apis, imported_apis)
        created_objs = models.API.objects.bulk_create(objs=new_apis)
        bulk_update(update_apis)

        created_apis_count = len(created_objs)
        updated_apis_count = len(update_apis)
        resp = {
                "createdCount": created_apis_count,
                "updatedCount": updated_apis_count,
        }
        logger.info(f"导入完成， {created_apis_count=}, {updated_apis_count=}")
        resp.update(response.YAPI_ADD_SUCCESS)
        return Response(resp)