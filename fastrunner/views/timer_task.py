# !/usr/bin/python3

# @Author:梨花菜
# @File: timer_task.py
# @Time : 2018/12/29 13:44
# @Email: lihuacai168@gmail.com
# @Software: PyCharm
import datetime

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
        body = eval(content["body"])

        if "base_url" in body["request"].keys():
            config = eval(models.Config.objects.get(name=body["name"], project__id=project_id).body)
            continue
        testcase_list.append(body)

    summary = debug_api(testcase_list, project_id, name=name, config=config, save=False)

    save_summary(
        f"{name}_" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        summary,
        project_id,
        type=3,
    )

    ding_message = DingMessage(run_type)
    ding_message.send_ding_msg(summary)
