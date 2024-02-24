# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: faker_helper.py
# @Time : 2021/8/6 16:13
# @Email: lihuacai168@gmail.com
from faker import Faker

F = Faker(locale="zh_CN")

# 假名f_name()
# 假地址f_addr()
# 假电话f_phone()

f_name = lambda: F.name()
f_addr = lambda: F.address()
f_phone = lambda: F.phone_number()
f_time = lambda: F.time()
f_date = lambda: F.date()
