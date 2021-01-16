# -*- coding: utf-8 -*-
# @Time    : 2020/8/11 16:12
# @Author  : lihuacai
# @Email   : lihuacai168@gmail.com
# @File    : lark_message.py
# @Software: PyCharm
import requests
import json
from fastrunner import models
from django.conf import settings


def get_base_post_content():
    return {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "",
                    "content": [
                    ]
                }
            }
        }
    }


def parse_message(summary: dict, msg_type: str):
    task_name = summary["task_name"]
    rows_count = summary['stat']['testsRun']
    pass_count = summary['stat']['successes']
    fail_count = summary['stat']['failures']
    error_count = summary['stat']['errors']
    duration = '%.2fs' % summary['time']['duration']
    report_id = models.Report.objects.last().id
    base_url = settings.IM_REPORT_SETTING.get('base_url')
    port = settings.IM_REPORT_SETTING.get('port')
    report_url = f'{base_url}:{port}/api/fastrunner/reports/{report_id}/'
    executed = rows_count
    fail_rate = '{:.2%}'.format(fail_count / executed)
    # 富文本
    if msg_type == 'post':
        msg_template = get_base_post_content()
        content = [[{'text': f'任务名称:{task_name}'}],
                   [{'text': f'总共耗时: {duration}'}],
                   [{'text': f'成功接口: {pass_count}'}],
                   [{'text': f'异常接口: {error_count}'}],
                   [{'text': f'失败接口: {fail_count}'}],
                   [{'text': f'失败比例: {fail_rate}'}],
                   [{'text': f'查看详情: {report_url}'}]]
        for d in content:
            d[0].update({'tag': 'text'})
        msg_template['content']['post']['zh_cn']['content'] = content
        return msg_template
    text = f" 任务名称: {task_name}\n 总共耗时: {duration}\n 成功接口: {pass_count}个\n 异常接口: {error_count}个\n 失败接口: {fail_count}个\n 失败比例: {fail_rate}\n 查看详情: {report_url}"
    return text


def send_message(summary: dict, webhook: str):
    """

    """
    # v1 https://open.feishu.cn/open-apis/bot/hook/xxx
    # v2 https://open.feishu.cn/open-apis/bot/v2/hook/xxx
    title = settings.IM_REPORT_SETTING.get('report_title')
    platform_name = settings.IM_REPORT_SETTING.get('platform_name', 'FasterRunner测试平台')
    if platform_name:
        title = platform_name + title
    version = webhook[37:39]
    if version == 'v2':
        msg = parse_message(summary=summary, msg_type='post')
        msg['content']['post']['zh_cn']['title'] = title
        data = msg
    else:
        msg = parse_message(summary=summary, msg_type=None)
        data = {
            "title": title,
            "text": msg
        }
    requests.post(url=webhook, data=json.dumps(data).encode("utf-8"))
