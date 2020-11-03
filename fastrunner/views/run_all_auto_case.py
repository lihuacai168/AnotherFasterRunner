# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: run_all_auto_case.py
# @Time : 2019/2/18 15:02
# @Email: lihuacai168@gmail.com
# @Software: PyCharm

from django.http import HttpResponse
import json
from fastrunner import models
from FasterRunner.mycelery import app
from djcelery.models import PeriodicTask
from fastrunner.views.timer_task import auto_run_testsuite_pk


def run_all_auto_case(request):
    run_type = request.GET.get('run_type')
    project = request.GET.get('project')
    task_name = 'fastrunner.tasks.schedule_debug_suite'
    query = PeriodicTask.objects.filter(
        enabled=1, task=task_name)
    if project:
        query = query.filter(description=project)
        # 默认报告类型是部署type=4
        report = models.Report.objects.filter(project_id=project, type=4).last()
        if report is None:
            models.Report.objects.filter(project_id=project).last()
        # 假设最后一条报告+1是刚刚执行的报告，有可能不准
        report_url = f'http://192.168.22.19:8000/api/fastrunner/reports/{report.id + 1}/'

    task_args_kwargs = query.values('args', 'kwargs')
    for i in task_args_kwargs:
        args = eval(i.get('args'))
        kwargs = eval(i.get('kwargs'))
        kwargs['run_type'] = run_type
        app.send_task(task_name, args=args, kwargs=kwargs)

    return HttpResponse(report_url)


# def run_all_auto_case(request):
#     # 运行方式 auto=定时执行 deploy=Jenkins部署执行
#     run_type = request.GET.get('run_type')
#     all_cases = get_all_auto_case()
#     if all_cases:
#         for pk, project_id in all_cases.items():
#             auto_run_testsuite_pk(pk=pk, project_id=project_id, run_type=run_type)
#         return HttpResponse("success")
#     else:
#         return HttpResponse("没有需要执行的用例集,如果需要增加自动执行用例集,在用例集的名字后面增加auto这个字段即可")


def get_all_auto_case():
    # 所有case
    all_case = models.Case.objects.all()

    # 自动用例集字典
    auto_case_dict = dict()

    for case in all_case:
        if 'auto' in case.name:
            auto_case_dict[case.id] = case.project_id

    return auto_case_dict
