# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: database.py 
# @Time : 2019/6/13 17:08
# @Email: lihuacai168@gmail.com
# @Software: PyCharm
import platform


class AutoChoiceDataBase:

    def db_for_read(self, model, **hints):
        run_system = platform.system()
        is_windows = run_system == 'Windows'
        if is_windows:
            return 'default'
        else:
            return 'remote'

    def db_for_write(self, model, **hints):
        run_system = platform.system()
        is_windows = run_system == 'Windows'
        if is_windows:
            return 'default'
        else:
            return 'remote'
