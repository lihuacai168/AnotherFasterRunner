# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: api_rig.py 
# @Time : 2019/5/25 9:25
# @Email: lihuacai168@gmail.com
# @Software: PyCharm
import datetime

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from rest_framework.viewsets import GenericViewSet
from fastrunner import models, serializers
from rest_framework.response import Response
from fastrunner.utils import response
from fastrunner.utils.decorator import request_log
from fastrunner.utils.parser import Format
from django.db import DataError
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from fastuser import models as user_model
from fastrunner.utils.relation import API_RELATION, API_AUTHOR
from fastrunner.views import run


class Authenticator(BaseAuthentication):
    """
    账户鉴权认证 token
    """

    def authenticate(self, request):
        token = request.query_params.get("token", None)
        obj = user_model.UserToken.objects.filter(token=token).first()

        if not obj:
            raise exceptions.AuthenticationFailed({
                "code": "9999",
                "msg": "用户未认证",
                "success": False
            })
        # valid update valid time
        obj.token = token
        obj.save()

        return obj.user, obj

    def authenticate_header(self, request):
        return 'Auth Failed'


class APIRigView(GenericViewSet):
    authentication_classes = [Authenticator, ]
    serializer_class = serializers.APISerializer
    queryset = models.API.objects

    def list(self, request):
        """
        接口列表 {
            project: int,
            node: int
        }
        """

        node = request.query_params["node"]
        project = request.query_params["project"]
        search = request.query_params["search"]
        # queryset = self.get_queryset().filter(project__id=project).order_by('-update_time')
        queryset = self.get_queryset().filter(project__id=project, delete=0).order_by('-update_time')
        # queryset = self.get_queryset().filter(Q(project__id=project) and ~Q(delete=1)).order_by('-update_time')

        if search != '':
            queryset = queryset.filter(name__contains=search)

        if node != '':
            queryset = queryset.filter(relation=node)

        pagination_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pagination_queryset, many=True)

        return self.get_paginated_response(serializer.data)

    @method_decorator(request_log(level='INFO'))
    def add(self, request):
        """
        新增一个接口
        {
  "header": {
    "header": {
      "wb-token": "$wb_token"
    },
    "desc": {
      "wb-token": "用户登陆token"
    }
  },
  "request": {
    "form": {
      "data": {},
      "desc": {}
    },
    "json": {},
    "params": {
      "params": {
        "goodsCode": "42470"
      },
      "desc": {
        "goodsCode": "商品编码"
      }
    },
    "files": {
      "files": {},
      "desc": {}
    }
  },
  "extract": {
    "extract": [],
    "desc": {}
  },
  "validate": {
    "validate": [{"equals": ["content.info.error",0]}]
  },
  "variables": {
    "variables": [
      {
        "auth_type": "APP_MEMBER_AUTH"
      },
      {
        "rpc_Group": "wbiao.seller.prod"
      },
      {
        "rpc_Interface": "cn.wbiao.seller.api.GoodsDetailService"
      },
      {
        "params_type": "Key_Value"
      },
      {
        "author": "xuqirong"
      }
    ],
    "desc": {
      "auth_type": "认证类型",
      "rpc_Group": "RPC服务组",
      "rpc_Interface": "后端服务接口",
      "params_type": "入参数形式",
      "author": "作者"
    }
  },
  "hooks": {
    "setup_hooks": [
      "${get_sign($request,$auth_type)}"
    ],
    "teardown_hooks": []
  },
  "url": "/wxmp/mall/goods/detail/getRecommendGoodsList",
  "method": "GET",
  "name": "查询关联的商品推荐列表-小程序需签名",
  "times": 1,
  "nodeId": "member",
  "project": 5,
  "rig_id":200014
}
        """

        api = Format(request.data)
        api.parse()
        # try:
        #     rig_env = api.rig_env
        # except KeyError:
        #     # 不传环境,使用默认测试环境0
        #     rig_env = 0
        try:
            relation = API_RELATION[api.relation]
        except KeyError:
            relation = API_RELATION['default']

        merge_name = api.name + '-' + str(api.rig_id)

        if api.rig_env == 0:
            merge_name += '-测试'

        elif api.rig_env == 1:
            merge_name += '-生产'
            # 生产环境比测试环境的关系节点大20
            relation += 20
        else:
            merge_name += '-预发布'

        api.testcase['name'] = merge_name
        api_body = {
            'name': merge_name,
            'body': api.testcase,
            'url': api.url,
            'method': api.method,
            'project': models.Project.objects.get(id=api.project),
            # 'relation': api.relation,
            'rig_id': api.rig_id,
            'rig_env': api.rig_env,
            'relation': relation
        }
        # try:
        #     relation = API_RELATION[api.relation]
        # except KeyError:
        #     relation = API_RELATION['default']

        # api_body['relation'] = relation
        try:
            # 增加api之前先删除已经存在的相同id的除了手动调试成功的api
            models.API.objects.filter(rig_id=api.rig_id).filter(~Q(tag=1)).update(delete=1,
                                                                                  update_time=datetime.datetime.now())
            # 创建成功,返回对象,方便获取id
            obj = models.API.objects.create(**api_body)
        except DataError:
            return Response(response.DATA_TO_LONG)

        # api作者
        # 2019年10月22日 修复rig增加api运行失败时,没有复制api到Java同学项目
        author = api_body['body']['variables'][4]['author']
        self.copy_to_java(api.rig_id, author)

        # api运行成功,就自动增加到用例集里面
        run_result = run.auto_run_api_pk(config=api.rig_env, id=obj.id)
        if run_result == 'success':
            run.update_auto_case_step(**api_body)

        return Response(response.API_ADD_SUCCESS)

    # 复制一份到Java同学项目
    def copy_to_java(self, rig_id, author):
        # 根据作者决定分组
        try:
            relation = API_AUTHOR[author]
        except KeyError:
            relation = API_AUTHOR['default']

        # Java项目的id=4
        # obj = models.API.objects.get(rig_id=rig_id)
        # 修复已经存在的rig_id的api无法复制
        obj = models.API.objects.filter(rig_id=rig_id).order_by('-id')[0]
        obj.id = None
        obj.relation = relation
        obj.project_id = 4
        obj.save()

    @method_decorator(request_log(level='INFO'))
    def update(self, request, **kwargs):
        """
        更新接口
        """
        pk = kwargs['rig_id']
        api = Format(request.data)
        api.parse()

        api_body = {
            'name': api.name,
            'body': api.testcase,
            'url': api.url,
            'method': api.method,
        }

        try:
            models.API.objects.filter(rig_id=pk).update(**api_body)
        except ObjectDoesNotExist:
            return Response(response.API_NOT_FOUND)
        return Response(response.API_UPDATE_SUCCESS)
