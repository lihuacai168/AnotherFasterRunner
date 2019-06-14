# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: database.py 
# @Time : 2019/6/13 17:08
# @Email: lihuacai168@gmail.com
# @Software: PyCharm
import platform


class AutoChoiceDataBase:
    run_system = platform.system()
    is_windows = run_system == 'Windows'

    def db_for_read(self, model, **hints):
        if self.is_windows:
            return 'default'
        else:
            return 'remote'

    def db_for_write(self, model, **hints):
        if self.is_windows:
            return 'default'
        else:
            return 'remote'
