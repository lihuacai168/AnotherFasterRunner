# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: timer_task.py 
# @Time : 2018/12/29 13:44
# @Email: lihuacai168@gmail.com
# @Software: PyCharm
from django.http import HttpResponse
from fastrunner import models
from fastrunner.utils import loader
from fastrunner.utils.ding_message import DingMessage


# 单个用例组
def auto_run_testsuite_pk(request):
    """
    :param pk: int 用例组主键
    :param config: int 运行环境
    :param project_id: int 项目id
    :return:
    """
    # 请求URL
    # url = 'http://localhost:8000/auto_run_pk/?pk=7&config=3&project_id=1'

    pk = request.GET.get('pk')
    config = request.GET.get('config')
    project_id = request.GET.get('project_id')

    # 通过主键获取单个用例
    test_list = models.CaseStep.objects. \
        filter(case__id=pk).order_by("step").values("body")

    # 把用例加入列表
    testcase_list = []
    for content in test_list:
        testcase_list.append(eval(content["body"]))

    summary = loader.debug_api(testcase_list, config, project_id)

    ding_message = DingMessage()
    ding_message.send_ding_msg(summary)

    return HttpResponse("success")


