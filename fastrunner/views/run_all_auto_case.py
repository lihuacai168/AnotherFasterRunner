# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: run_all_auto_case.py 
# @Time : 2019/2/18 15:02
# @Email: lihuacai168@gmail.com
# @Software: PyCharm

import requests

from django.http import HttpResponse
from fastrunner import models


def run_all_auto_case(request):
    # 运行方式 auto=定时执行 deploy=Jenkins部署执行
    run_type = request.GET.get('run_type')
    all_cases = get_all_auto_case()
    if all_cases:
        for pk,project_id in all_cases.items():
            url = "http://{2}:8000/auto_run_testsuite_pk/?pk={0}&project_id={1}&run_type={3}"\
                .format(pk, project_id, get_local_ip(), run_type)
            requests.get(url)
        return HttpResponse("success")
    else:
        return HttpResponse("没有需要执行的用例集,如果需要增加自动执行用例集,在用例集的名字后面增加auto这个字段即可")


def get_all_auto_case():
    # 所有case
    all_case = models.Case.objects.all()

    # 自动用例集字典
    auto_case_dict = dict()

    for case in all_case:
        if 'auto' in case.name:
            auto_case_dict[case.id] = case.project_id

    return auto_case_dict


def get_local_ip():
    import socket
    # 获取本机电脑名
    hostname = socket.getfqdn(socket.gethostname())
    # 获取本机ip
    ip_addr = socket.gethostbyname(hostname)
    return ip_addr
