# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: run_all_auto_case.py
# @Time : 2019/2/18 15:02
# @Email: lihuacai168@gmail.com
# @Software: PyCharm

from django.http import HttpResponse, JsonResponse
from django.conf import settings
import json
from fastrunner import models
from FasterRunner.mycelery import app
from djcelery.models import PeriodicTask

from fastrunner.utils.host import parse_host



def run_all_auto_case(request):
    run_type = request.GET.get('run_type', 'deploy')
    project = request.GET.get('project')
    user = request.GET.get('user', 'CICD')
    task_ids: str = request.GET.get('task_ids')
    task_name = 'fastrunner.tasks.schedule_debug_suite'
    query = PeriodicTask.objects.filter(
        enabled=1, task=task_name)
    if project:
        query = query.filter(description=project)
    if task_ids:
        query = query.filter(id__in=task_ids.split(','))

    task_args_kwargs = query.values('args', 'kwargs')
    for i in task_args_kwargs:
        args = eval(i.get('args'))
        kwargs = json.loads(i.get('kwargs'))
        kwargs['run_type'] = run_type
        kwargs['user'] = user
        kwargs['task_id'] = i.get('task_id')
        app.send_task(task_name, args=args, kwargs=kwargs)
    return JsonResponse({'success': True, "run_tasks": len(query)})


def build_testsuite(project: int, config_id: int = 0, testcase_tag: int = 1):
    """
    组装可运行的用例
    """
    cases = list(models.Case.objects.filter(project__id=project, tag=testcase_tag).order_by('id').values('id', 'name'))
    test_sets = []
    config_list = []
    host = '请选择'
    reload_config = None
    if config_id:
        # 前端有指定config，会覆盖用例本身的config
        reload_config = eval(models.Config.objects.get(id=config_id).body)
    for case in cases:
        test_list = models.CaseStep.objects.filter(case__id=case["id"]).order_by("step").values("body")
        testcase_list = []
        for content in test_list:
            body = eval(content["body"])
            if body["request"].get('url'):
                testcase_list.append(parse_host(host, body))
            elif body["request"].get('base_url'):
                if reload_config is None:
                    config = eval(models.Config.objects.get(name=body["name"], project__id=project).body)
                else:
                    config = reload_config
        config_list.append(parse_host(host, config))
        test_sets.append(testcase_list)
    return {'suite': test_sets, 'obj': cases, 'config': config_list}


def get_report_url(request):
    """
    获取项目最后一条部署类型的报告
    """
    project = request.GET.get('project')
    # 默认报告类型是部署type=4
    report = models.Report.objects.filter(project_id=project, type=4).last()
    if report is None:
        models.Report.objects.filter(project_id=project).last()
    report_url = f'{settings.BASE_REPORT_URL}/{report.id}/'
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
