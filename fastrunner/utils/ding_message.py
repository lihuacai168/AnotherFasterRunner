# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: ding_message.py 
# @Time : 2018/12/21 15:11
# @Email: lihuacai168@gmail.com
# @Software: PyCharm
from dingtalkchatbot.chatbot import DingtalkChatbot


class DingMessage:
    """
    调用钉钉机器人发送测试结果
    """

    def __init__(self):
        webhook = 'https://oapi.dingtalk.com/robot/send?access_token=998422738ca7d32f8641e9369da7f1b5545aa09c8fcec5ae17324e609c5d1af0'
        self.robot = DingtalkChatbot(webhook)

    def send_ding_msg(self,summary):
        """
        sum['details'][0]['records']
        name = sum['details'][0]['records'][0]['name']
        status = sum['details'][0]['records'][0]['status']
        url = sum['details'][0]['records'][0]['meta_data']['request']['url']
        expect = sum['details'][0]['records'][0]['meta_data']['validators'][0]['expect']
        check_value = sum['details'][0]['records'][0]['meta_data']['validators'][0]['check_value']

        :param summary:
        :return:
        """
        # summary['stat'] = {'testsRun': 2, 'failures': 1, 'errors': 0, 'skipped': 0, 'expectedFailures': 0, 'unexpectedSuccesses': 0,'successes': 1}
        rows_count = summary['stat']['testsRun']
        pass_count = summary['stat']['successes']
        fail_count = summary['stat']['failures']
        skip_row = summary['stat']['skipped']

        # 已执行的条数
        executed = rows_count
        title = '自动化测试报告'
        # 通过率
        pass_rate = '{:.2%}'.format(pass_count / executed)

        # 失败率
        fail_rate = '{:.2%}'.format(fail_count / executed)

        # fail_count_list[0] {"name": name, "url": url, expect":[],"check_value":[]}
        fail_count_list = []

        # 失败详情
        if fail_count == 0:
            fail_detail = ''

        else:
            details = summary['details']
            print(details)
            for detail in details:
                for record in detail['records']:
                    print(record['meta_data']['validators'])
                    if record['status'] != 'failure':
                        continue
                    else:
                        url_fail = record['meta_data']['request']['url']
                        case_name = record['name']
                        expect = []
                        check_value = []
                        for validator in record['meta_data']['validators']:
                            expect.append(validator['expect'])
                            check_value.append(validator['check_value'])
                        fail_count_list.append({'case_name': case_name, 'url': url_fail, 'expect':expect, 'check_value':check_value})

            fail_detail  = '失败的接口是:\n'
            for i in fail_count_list:
                s = '用例名:{0} 请求url:{1}\n 期望值:{2}\n 返回结果:{3} \n'.format(i["case_name"], i["url"], i["expect"], i["check_value"])
                fail_detail += s

        msg = '''{0}:
总用例{1}共条,执行了{2}条,跳过{3}条.
通过{4}条,通过率{5}.
失败{6}条,失败率{7}.
{8}'''.format(title, rows_count, executed, skip_row, pass_count, pass_rate, fail_count, fail_rate,fail_detail)

        print(msg)
        # self.robot.send_text(msg)

if __name__ == '__main__':
    robot = DingMessage()
    summary = {'stat':{'testsRun': 2, 'failures': 0, 'errors': 0, 'skipped': 0, 'expectedFailures': 0,
                       'unexpectedSuccesses': 0, 'successes': 1}}
    robot.send_ding_msg(summary)