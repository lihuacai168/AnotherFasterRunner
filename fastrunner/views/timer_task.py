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
    # 用例集中固定配置:http://localhost:8000/auto_run_testsuite_pk/?pk=11&config=4&project_id=1

    pk = request.GET.get('pk')
    run_type = request.GET.get('run_type')
    # config = request.GET.get('config')
    config = None
    project_id = request.GET.get('project_id')
    # name = request.GET.get('name')
    name = models.Case.objects.get(pk = pk).name

    # 通过主键获取单个用例
    test_list = models.CaseStep.objects. \
        filter(case__id=pk).order_by("step").values("body")

    # 把用例加入列表
    testcase_list = []
    for content in test_list:
        # testcase_list.append(eval(content["body"]))
        body = eval(content["body"])

        if "base_url" in body["request"].keys():
            config = eval(models.Config.objects.get(name=body["name"], project__id=project_id).body)
            continue
        testcase_list.append(body)

    # summary = loader.debug_api(testcase_list, config, project_id)
    summary = loader.debug_api(testcase_list, project_id, name=name, config=config)

    ding_message = DingMessage(run_type)
    ding_message.send_ding_msg(summary)

    return HttpResponse("success")


