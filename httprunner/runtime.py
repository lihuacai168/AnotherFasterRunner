# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: runtime.py
# @Time : 2021/8/1 12:44
# @Email: lihuacai168@gmail.com
import threading

import pydash

from httprunner.runner import Runner


class Hrun(object):
    """
    特殊关键字，提供给驱动函数中使用
    可以在驱动函数中，修改配置变量和用例步骤运行时变量
    """

    @staticmethod
    def get_current_context():
        current_thread = threading.current_thread().name
        if Runner.instances.get(current_thread):
            return Runner.instances[current_thread].context
        return Runner().context

    @staticmethod
    def set_config_var(name, value):
        # 在运行时修改配置变量
        current_context = Hrun.get_current_context()
        current_context.TESTCASE_SHARED_VARIABLES_MAPPING[name] = value

    @staticmethod
    def set_config_header(name, value):
        # 在运行时修改配置中请求头的信息
        # 比如: 用例中需要切换账号，实现同时请求头中token和userId
        current_context = Hrun.get_current_context()
        pydash.set_(current_context.TESTCASE_SHARED_REQUEST_MAPPING, f'headers.{name}', value)

    @staticmethod
    def set_step_var(name, value):
        current_context = Hrun.get_current_context()
        current_context.testcase_runtime_variables_mapping[name] = value