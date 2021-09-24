# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: ci.py
# @Time : 2021/5/25 15:51
# @Email: lihuacai168@gmail.com
import datetime
import json
import re
import time

import xmltodict
from django.http import HttpResponse
from django.conf import settings
from djcelery.models import PeriodicTask
from drf_yasg.utils import swagger_auto_schema

from fastrunner import models
from fastrunner.utils import loader, lark_message
from fastrunner.utils.decorator import request_log
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from fastrunner.serializers import CISerializer, CIReportSerializer
from fastrunner.utils.host import parse_host
from fastrunner.utils.loader import save_summary


def summary2junit(summary: dict) -> dict:
    res = {
        "testsuites": {
            "testsuite": {
                "errors": 0,
                "failures": 0,
                "hostname": "",
                "name": "",
                "skipped": 0,
                "tests": 0,
                "time": "0",
                "timestamp": "20210524T18:04:50.941913",
                "testcase": []
            }
        }
    }

    time_info = summary.get('time')
    res["testsuites"]["testsuite"]["time"] = time_info.get('duration')
    start_at: str = time_info.get('start_at')
    datetime_str = datetime.datetime.fromtimestamp(int(float(start_at))).strftime('%Y-%m-%dT%H:%M:%S.%f')
    res["testsuites"]["testsuite"]["timestamp"] = datetime_str

    details = summary.get('details', [])
    res["testsuites"]["testsuite"]["tests"] = len(details)
    for detail in details:
        test_case = {
            "classname": "",
            "file": "",
            "line": "",
            "name": "",
            "time": ""
        }
        name = detail.get('name')
        test_case['classname'] = name  # 对应junit的Suite
        records = detail.get('records')
        test_case['line'] = len(records)
        test_case['time'] = detail['time']['duration']
        result = detail.get('success')
        step_names = []
        for index, record in enumerate(records):
            step_names.append(f"{index}-{record['name']}")
        test_case['name'] = '\n'.join(step_names)  # 对应junit的每个case的Name

        # 记录错误case的详细信息
        case_error = False
        if result is False:
            failure_details = []
            for index, record in enumerate(records):
                step_status = record.get('status')
                if step_status == 'failure':
                    failure_details.append(
                        f"{index}-{record['name']}" + '\n' + record.get('attachment') + '\n' + '*' * 68)
                elif step_status == 'error':
                    case_error = True
            else:
                # 用例步骤中有error，整个用例算为error
                if case_error:
                    res["testsuites"]["testsuite"]["errors"] += 1
                else:
                    res["testsuites"]["testsuite"]["failures"] += 1

            failure = {
                "message": "断言或者抽取失败",
                "#text": '\n'.join(failure_details)
            }
            test_case['failure'] = failure
        res["testsuites"]["testsuite"]["testcase"].append(test_case)
    return res


class CIView(GenericViewSet):
    authentication_classes = []
    serializer_class = CISerializer
    pagination_class = None

    @swagger_auto_schema(operation_summary='gitlab-ci触发自动化用例运行')
    @method_decorator(request_log(level='DEBUG'))
    def run_ci_tests(self, request):
        """
        gitlab-ci发起请求
        测试平台解析参数，定时任务中的ci_project_id和ci_env同时匹配时，才会触发执行任务
        """
        ser = CISerializer(data=request.data)
        if ser.is_valid():
            task_name = 'fastrunner.tasks.schedule_debug_suite'
            ci_project_id: int = ser.validated_data.get('ci_project_id')
            ci_env: str = ser.validated_data.get('env')

            query = PeriodicTask.objects.filter(
                enabled=1, task=task_name)
            pk_kwargs_list = query.values('pk', 'kwargs', 'description')
            enabled_task_ids = []
            project = None
            for pk_kwargs in pk_kwargs_list:
                pk: int = pk_kwargs['pk']
                kwargs: dict = json.loads(pk_kwargs['kwargs'])
                ci_project_ids: list = eval(kwargs.get('ci_project_ids') or '[]')
                if isinstance(ci_project_ids, int):
                    ci_project_ids = [ci_project_ids]

                # 定时任务中的ci_project_id和ci_env同时匹配
                if ci_project_id in ci_project_ids and ci_env and ci_env == kwargs.get('ci_env'):
                    enabled_task_ids.append(pk)
                    project = pk_kwargs['description']

            # 没有匹配用例，直接返回
            if not enabled_task_ids:
                datetime_str = datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%dT%H:%M:%S.%f')
                not_found_case_res = {
                    "testsuites": {
                        "testsuite": {
                            "errors": 0,
                            "failures": 0,
                            "hostname": "",
                            "name": "没有找到匹配的用例",
                            "skipped": 0,
                            "tests": 0,
                            "time": "0",
                            "timestamp": datetime_str,
                            "testcase": []
                        }
                    }
                }

                xml_data = xmltodict.unparse(not_found_case_res)
                return HttpResponse(xml_data, content_type='text/xml')

            test_sets = []
            suite_list = []
            config_list = []
            host = "请选择"
            config = None
            webhook_set = set()
            override_config_body = None
            for task_id in enabled_task_ids:
                task_obj: str = query.filter(id=task_id).first()
                # 如果task中存在重载配置，就覆盖用例中的配置
                override_config = json.loads(task_obj.kwargs).get('config')
                if override_config_body is None and override_config and override_config != "请选择":
                    override_config_body = eval(
                        models.Config.objects.get(name=override_config, project__id=project).body)

                if task_obj:
                    # 判断webhook是否合法
                    case_ids: str = task_obj.args
                    url = json.loads(task_obj.kwargs).get('webhook')
                    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                    if re.match(url_pattern, url):
                        webhook_set.add(url)
                else:
                    continue
                # 反查出一个task中包含的所有用例
                suite = list(models.Case.objects.filter(pk__in=eval(case_ids)).order_by('id').values('id', 'name'))
                for case in suite:
                    case_step_list = models.CaseStep.objects. \
                        filter(case__id=case["id"]).order_by("step").values("body")
                    testcase_list = []
                    for case_step in case_step_list:
                        body = eval(case_step["body"])
                        if body["request"].get('url'):
                            testcase_list.append(parse_host(host, body))
                        elif config is None and body["request"].get('base_url'):
                            # 当前步骤是配置
                            # 如果task中存在重载配置，就覆盖用例中的配置
                            if override_config_body:
                                config = override_config_body
                            else:
                                config = eval(models.Config.objects.get(name=body["name"], project__id=project).body)
                    config_list.append(parse_host(host, config))
                    test_sets.append(testcase_list)
                    config = None
                suite_list.extend(suite)
                override_config_body = None
            # 同步运行用例
            summary, _ = loader.debug_suite(test_sets, project, suite_list, config_list, save=False)
            ci_project_namespace = ser.validated_data['ci_project_namespace']
            ci_project_name = ser.validated_data['ci_project_name']
            ci_job_id = ser.validated_data['ci_job_id']
            summary['name'] = f"{ci_project_namespace}_{ci_project_name}_job{ci_job_id}"

            report_id = save_summary(summary.get('name'), summary, project, type=4, user=ser.validated_data['start_job_user'],
                         ci_metadata=ser.validated_data)
            junit_results = summary2junit(summary)
            xml_data = xmltodict.unparse(junit_results)
            summary['task_name'] = 'gitlab-ci_' + summary.get('name')
            summary['report_id'] = report_id
            for webhook in webhook_set:
                lark_message.send_message(summary=summary, webhook=webhook,
                                          ci_job_url=ser.validated_data['ci_job_url'],
                                          ci_pipeline_url=ser.validated_data['ci_pipeline_url'],
                                          case_count=junit_results['testsuites']['testsuite']['tests'])
            return HttpResponse(xml_data, content_type='text/xml')
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(query_serializer=CIReportSerializer, operation_summary='获取gitlab-ci运行的报告url')
    def get_ci_report_url(self, request):
        ser = CIReportSerializer(data=request.query_params)
        if ser.is_valid():
            ci_job_id = ser.validated_data['ci_job_id']
            report_obj = models.Report.objects.filter(ci_job_id=ci_job_id).first()
            if report_obj:
                report_url = f'{settings.BASE_REPORT_URL}/{report_obj.id}/'
            else:
                return Response(data=f'查找的ci_job_id: {ci_job_id}不存在')
            return Response(data=report_url)
        else:
            return Response(data=ser.errors, status=status.HTTP_400_BAD_REQUEST)
