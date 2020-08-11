# -*- coding: utf-8 -*-
# @Time    : 2020/8/11 16:12
# @Author  : lihuacai
# @Email   : lihuacai168@gmail.com
# @File    : lark_message.py
# @Software: PyCharm
import requests
import json
from fastrunner import models


def parse_message(summary: dict):
    task_name = summary["task_name"]
    rows_count = summary['stat']['testsRun']
    pass_count = summary['stat']['successes']
    fail_count = summary['stat']['failures']
    error_count = summary['stat']['errors']
    duration = '%.2fs' % summary['time']['duration']
    report_id = models.Report.objects.last().id
    report_url = f'http://192.168.17.107:8000/api/fastrunner/reports/{report_id}/'
    executed = rows_count
    fail_rate = '{:.2%}'.format(fail_count / executed)
    text = f" 任务名称: {task_name}\n 总共耗时: {duration}\n 成功接口: {pass_count}个\n 异常接口: {error_count}个\n 失败接口: {fail_count}个\n 失败比例: {fail_rate}\n 查看详情: {report_url}"
    return text


def send_message(summary: dict, webhook: str):
    msg = parse_message(summary=summary)
    data = {
        "title": "FasterRunner接口自动化测试报告",
        "text": msg
    }
    requests.post(url=webhook, data=json.dumps(data).encode("utf-8"))
