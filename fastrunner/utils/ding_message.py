# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: ding_message.py 
# @Time : 2018/12/21 15:11
# @Email: lihuacai168@gmail.com
# @Software: PyCharm
from dingtalkchatbot.chatbot import DingtalkChatbot

from fastrunner.utils.parser import format_summary_to_ding


class DingMessage:
    """
    调用钉钉机器人发送测试结果
    """

    def __init__(self, run_type):
        self.run_type = run_type
        if run_type == 'auto':
            webhook = 'https://oapi.dingtalk.com/robot/send?access_token=998422738ca7d32f8641e9369da7f1b5545aa09c8fcec5ae17324e609c5d1af0'
            # webhook = 'https://oapi.dingtalk.com/robot/send?access_token=cb1ece248f594144a11bc0cf467ae4fd0f73beb3133f6a79b16d07ef23da0a59' # 调试机器人
        elif run_type == 'deploy':
            webhook = 'https://oapi.dingtalk.com/robot/send?access_token=16c4dbf613c5f1f288bbf695c1997ad41d37ad580d94ff1a0b7ceae6797bbc70'
            # webhook = 'https://oapi.dingtalk.com/robot/send?access_token=cb1ece248f594144a11bc0cf467ae4fd0f73beb3133f6a79b16d07ef23da0a59' # 调试机器人
        self.robot = DingtalkChatbot(webhook)

    def send_ding_msg(self, summary, report_name=None):
        msg_and_fail_count = format_summary_to_ding('markdown', summary, report_name=report_name)
        msg = msg_and_fail_count[0]
        fail_count = msg_and_fail_count[1]
        title = 'FasterRunner自动化测试报告'

        if fail_count == 0:
            if self.run_type == 'deploy':
                print("deploy_success")
            elif self.run_type == 'auto':
                self.robot.send_markdown(title=title, text=msg)
        else:
            if self.run_type == 'deploy':
                self.robot.send_markdown(title=title, text=msg, is_at_all=True)
            elif self.run_type == 'auto':
                receive_msg_mobiles = [18666126234, 18122118571, 13763312220, 15989041619, 18665742877,
                                       13512756535]  # 接收钉钉消息的列表
                at_phone = ''
                for phone in [f'@{phone} ' for phone in receive_msg_mobiles]:
                    at_phone += phone
                msg += at_phone
                self.robot.send_markdown(title=title, text=msg, at_mobiles=receive_msg_mobiles)


if __name__ == '__main__':
    robot = DingMessage()
    summary = {'stat':{'testsRun': 2, 'failures': 0, 'errors': 0, 'skipped': 0, 'expectedFailures': 0,
                       'unexpectedSuccesses': 0, 'successes': 1}}
    robot.send_ding_msg(summary)
