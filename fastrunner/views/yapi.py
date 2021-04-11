# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: yapi.py
# @Time : 2021/3/31 22:56
# @Email: lihuacai168@gmail.com
from rest_framework.views import APIView
from rest_framework.response import Response

from fastrunner.utils.parser import Yapi
from fastrunner.utils import response
from fastrunner import models


class YAPIView(APIView):

    def post(self, request, **kwargs):
        faster_project_id = kwargs['pk']
        token = request.data['yapi_openapi_token']
        yapi_base_url = request.data['yapi_base_url']
        yapi = Yapi(yapi_base_url=yapi_base_url, token=token, faster_project_id=faster_project_id)

        # 获取yapi的分组，然后更新api tree
        yapi.create_relation_id(yapi.fast_project_id)

        # 获取yapi所有的api的id
        yapi.get_api_ids()

        # 通过id获取所有api的详情
        yapi.get_api_info()

        # 把yapi解析成符合faster的api格式
        parsed_apis: list = yapi.get_parsed_apis()
        objs = models.API.objects.bulk_create(objs=parsed_apis)
        parsed_apis_count = len(parsed_apis)
        saved_apis_count = len(objs)
        failed_count = parsed_apis_count - saved_apis_count
        resp = {"获取api个数": parsed_apis_count,
                "实际导入api个数": saved_apis_count,
                "失败api个数": failed_count}
        if failed_count > 0:
            resp.update(response.YAPI_ADD_FAILED)
        else:
            resp.update(response.YAPI_ADD_SUCCESS)
        return Response(resp)