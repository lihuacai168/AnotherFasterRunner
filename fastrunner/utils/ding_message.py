# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: ding_message.py
# @Time : 2018/12/21 15:11
# @Email: lihuacai168@gmail.com
# @Software: PyCharm

import logging
# import os
# os.environ.setdefault(
#     "DJANGO_SETTINGS_MODULE", "FasterRunner.settings.dev"
# )
#
# import django
#
# django.setup()

from dingtalkchatbot.chatbot import DingtalkChatbot

from fastrunner.utils.parser import format_summary_to_ding

log = logging.getLogger(__name__)


class DingMessage:
    """
    调用钉钉机器人发送测试结果
    """

    def __init__(self, run_type: str = "auto", webhook: str = ""):
        self.run_type = run_type
        self.robot = DingtalkChatbot(webhook)

    def send_ding_msg(self, summary, report_name=None):
        msg_and_fail_count = format_summary_to_ding(
            "markdown", summary, report_name=report_name
        )
        msg = msg_and_fail_count[0]
        fail_count = msg_and_fail_count[1]
        title = "FasterRunner自动化测试报告"

        if fail_count == 0:
            if self.run_type == "deploy":
                print("deploy_success")
            elif self.run_type == "auto":
                self.robot.send_markdown(title=title, text=msg)
        else:
            if self.run_type == "deploy":
                self.robot.send_markdown(title=title, text=msg, is_at_all=True)
            elif self.run_type == "auto":
                receive_msg_mobiles = [
                    18666126235,
                ]  # 接收钉钉消息的列表
                at_phone = ""
                for phone in [f"@{phone} " for phone in receive_msg_mobiles]:
                    at_phone += phone
                msg += at_phone
                self.robot.send_markdown(
                    title=title, text=msg, at_mobiles=receive_msg_mobiles
                )


if __name__ == "__main__":
    import os

    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "FasterRunner.settings.dev"
    )

    import django

    django.setup()
    webhook: str = "https://oapi.dingtalk.com/robot/send?access_token=694e9cfa98612c9da56d0c190e73717ab13095c83a1302da075b946c8f3940b0"
    robot = DingMessage(webhook=webhook)
    summary = {
        "success": True,
        "stat": {
            "testsRun": 1,
            "failures": 0,
            "errors": 0,
            "skipped": 0,
            "expectedFailures": 0,
            "unexpectedSuccesses": 0,
            "successes": 1,
        },
        "time": {
            "start_at": 1682062407.668906,
            "setup_hooks_duration": 0,
            "teardown_hooks_duration": 0.0005848407745361328,
            "duration": 0.141,
        },
        "platform": {
            "httprunner_version": "1.5.15",
            "python_version": "CPython 3.9.11",
            "platform": "macOS-13.3.1-x86_64-i386-64bit",
        },
        "details": [
            {
                "success": True,
                "stat": {
                    "testsRun": 1,
                    "failures": 0,
                    "errors": 0,
                    "skipped": 0,
                    "expectedFailures": 0,
                    "unexpectedSuccesses": 0,
                    "successes": 1,
                },
                "time": {
                    "start_at": 1682062407.668906,
                    "setup_hooks_duration": 0,
                    "teardown_hooks_duration": 0.0005848407745361328,
                    "duration": 0.141,
                },
                "records": [
                    {
                        "name": "登录-成功",
                        "status": "success",
                        "attachment": "",
                        "meta_data": {
                            "request": {
                                "url": "http://localhost:8000/api/user/login/?s=d&sxx=dsx&sxx22=&sxx2=dsx&sx2x22=&d55555553d=sd&1s=d&2sxx=dsx&3sxx22=&4sxx2=dsx&4sx2x22=&5d55555553d=sd",
                                "method": "POST",
                                "headers": {
                                    "User-Agent": "python-requests/2.22.0",
                                    "Accept-Encoding": "gzip, deflate",
                                    "Accept": "*/*",
                                    "Connection": "keep-alive",
                                    "Content-Type": "application/json;charset=utf-8",
                                    "userId": "var",
                                },
                                "start_timestamp": 1682062407.671167,
                                "setup_hooks_start": 1682062407.670105,
                                "setup_hooks_duration": 0,
                                "json": {
                                    "username": "qa1",
                                    "password": "gg9tKGBjK8GEgg9tKGBjK8GE",
                                },
                                "verify": False,
                                "params": {
                                    "s": "d",
                                    "sxx": "dsx",
                                    "sxx22": "",
                                    "sxx2": "dsx",
                                    "sx2x22": "",
                                    "d55555553d": "sd",
                                    "1s": "d",
                                    "2sxx": "dsx",
                                    "3sxx22": "",
                                    "4sxx2": "dsx",
                                    "4sx2x22": "",
                                    "5d55555553d": "sd",
                                },
                                "body": '{"username": "qa1", "password": "gg9tKGBjK8GEgg9tKGBjK8GE"}',
                            },
                            "response": {
                                "status_code": 200,
                                "headers": {
                                    "Date": "Fri, 21 Apr 2023 07:33:27 GMT",
                                    "Server": "WSGIServer/0.2 CPython/3.9.11",
                                    "Content-Type": "application/json",
                                    "Vary": "Accept, Origin, Accept-Encoding",
                                    "Allow": "POST, OPTIONS",
                                    "X-Frame-Options": "SAMEORIGIN",
                                    "Content-Length": "277",
                                    "RESPONSE_HEADER_NAME": "fce1b7819ae7416c8bfe87afa37d78cb",
                                    "Content-Encoding": "gzip",
                                },
                                "content_size": 317,
                                "response_time_ms": 143.51,
                                "elapsed_ms": 140.834,
                                "encoding": None,
                                "content": '{"code":"0001","success":true,"msg":"login success","token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6InFhMSIsImV4cCI6MTcxMzU5ODQwNywiZW1haWwiOiJxYTFAcXEuY29tIiwib3JpZ19pYXQiOjE2ODIwNjI0MDd9.nFBrmUsariqGuZ3zZSao29yKjiOMmlhi3al6UoV2uCI","user":"qa1","is_superuser":false,"show_hosts":false}',
                                "content_type": "application/json",
                                "ok": True,
                                "url": "http://localhost:8000/api/user/login/?s=d&sxx=dsx&sxx22=&sxx2=dsx&sx2x22=&d55555553d=sd&1s=d&2sxx=dsx&3sxx22=&4sxx2=dsx&4sx2x22=&5d55555553d=sd",
                                "reason": "OK",
                                "cookies": {},
                                "text": '{"code":"0001","success":true,"msg":"login success","token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6InFhMSIsImV4cCI6MTcxMzU5ODQwNywiZW1haWwiOiJxYTFAcXEuY29tIiwib3JpZ19pYXQiOjE2ODIwNjI0MDd9.nFBrmUsariqGuZ3zZSao29yKjiOMmlhi3al6UoV2uCI","user":"qa1","is_superuser":false,"show_hosts":false}',
                                "teardown_hooks_start": 1682062407.815586,
                                "teardown_hooks_duration": 0.0005848407745361328,
                            },
                        },
                    }
                ],
                "name": "登录-成功",
                "base_url": "http://localhost:8000",
                "in_out": {
                    "in": {},
                    "out": {},
                },
            }
        ],
    }

    robot.send_ding_msg(summary)
