# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: rand_helper.py
# @Time : 2021/8/12 16:32
# @Email: lihuacai168@gmail.com
import random
import string
import uuid


def rand_int(begin: int = 0, end: int = 10000):
    """生成0-10000的随机数"""
    return random.randint(begin, end)


def rand_int4():
    """4位随机数"""
    return rand_int(1000, 9999)


def rand_int5():
    """5位随机数"""
    return rand_int(10000, 99999)


def rand_int6():
    """6位随机数"""
    return rand_int(100000, 999999)


def rand_str(n: int = 5):
    """获取大小写字母+数字的随机字符串，默认5位"""
    seq = string.ascii_letters + string.digits
    return "".join(random.choices(seq, k=n))


def uid():
    return str(uuid.uuid1())
