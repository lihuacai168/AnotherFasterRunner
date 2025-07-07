import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import DataError
from rest_framework.decorators import api_view
from rest_framework.response import Response

from djcelery import models as celery_models
from fastrunner import models, tasks
from fastrunner.utils import loader, response
from fastrunner.utils.host import parse_host
from fastrunner.utils.safe_json_parser import safe_json_loads

from fastrunner import models
from fastrunner.utils.ding_message import DingMessage
from fastrunner.utils.loader import debug_api, save_summary


# 单个用例组
def auto_run_testsuite_pk(**kwargs):
    """
    :param pk: int 用例组主键
    :param config: int 运行环境
    :param project_id: int 项目id
    :return:
    """

    pk = kwargs.get("pk")
    run_type = kwargs.get("run_type")
    project_id = kwargs.get("project_id")

    name = models.Case.objects.get(pk=pk).name

    # 通过主键获取单个用例
    test_list = models.CaseStep.objects.filter(case__id=pk).order_by("step").values("body")

    # 把用例加入列表
    testcase_list = []
    for content in test_list:
        body = safe_json_loads(content["body"])

        if "base_url" in body["request"].keys():
            config = safe_json_loads(models.Config.objects.get(name=body["name"], project__id=project_id).body)
            continue
        testcase_list.append(body)

    summary = debug_api(testcase_list, project_id, name=name, config=config, save=False)

    save_summary(f"{name}_" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), summary, project_id, type=3)

    ding_message = DingMessage(run_type)
    ding_message.send_ding_msg(summary)
