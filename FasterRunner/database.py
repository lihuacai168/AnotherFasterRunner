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
        if platform.system() == 'Windows':
            return 'default'
        else:
            return 'prod'

    def db_for_write(self, model, **hints):
        if platform.system() == 'Windows':
            return 'default'
        else:
            return 'prod'

