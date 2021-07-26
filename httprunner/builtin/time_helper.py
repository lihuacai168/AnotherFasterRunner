# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: time_helper.py
# @Time : 2021/7/26 18:26
# @Email: lihuacai168@gmail.com

import datetime
import time


def get_day(days: int = 0, **kwargs):
    """
    >>> get_day()
    20201015 # 今天的日期

    >>> get_day(1)
    20201016 # 明天的日期

    >>> get_day(-1)
    20201014 # 昨天的日期
    """
    d = datetime.timedelta(days)
    n = datetime.datetime.now()
    time_str = f"%Y%m%d"
    if kwargs:
        h = kwargs.get("h", "00")
        m = kwargs.get("m", "00")
        s = kwargs.get("s", "00")
        time_str = f"{time_str} {h}:{m}:{s}"
    return (n + d).strftime(time_str)


def get_day_h(days: int = 0, **kwargs):
    """
    >>> get_day_h(0,h=7)
    2021042207
    """
    d = datetime.timedelta(days)
    n = datetime.datetime.now()
    time_str = f"%Y%m%d"
    if kwargs:
        h = str(kwargs.get("h"))
        h = h.rjust(2, '0')
        time_str = f"{time_str}{h}"
    return (n + d).strftime(time_str)


# 获取时间戳
def get_ts(interval: int = 0, t=None):
    """
    >>> get_ts(0)
    1602752052 # 当前时间戳

    >>> get_ts(0,9)
    1602723600 # 今天9点的时间戳

    >>> get_ts(0,'9:15')
    1602723600 # 今天9点15分的时间戳

    >>> get_ts(0,'9:15:10')
    1602723600 # 今天9点15分10秒的时间戳
    """
    if isinstance(interval, int) == True and t is None:
        return str(int(time.time()) + interval)
    else:
        time_format = "%Y%m%d"
        t = str(t)
        if t.count(":") == 0 and len(t.split()) == 1:
            time_format = time_format + "%H"
        elif t.count(":") == 1 and len(t.split()) == 1:
            time_format = time_format + "%H:%M"
        elif t.count(":") == 2 and len(t.split()) == 1:
            time_format = time_format + "%H:%M:%S"
        time_arr = time.strptime(get_day(interval) + t, time_format)
        return int(time.mktime(time_arr))


def get_ts_int(interval: int = 0, t=None) -> int:
    return int(get_ts(interval, t))


def get_hour_ts(interval: int = 0) -> str:
    # 当前时间所在的小时，转换为时间戳
    # 2021-3-9 17:0:12, 取2021-3-9 17:0:0，然后转换为时间戳
    now_hour = int(datetime.datetime.now().replace(minute=0, second=0, microsecond=0).timestamp())
    return str(now_hour + interval * 3600)


def get_hour() -> str:
    # 获取当前的小时，不足两位补0
    return str(datetime.datetime.now().hour).rjust(2, '0')


def get_hour_ts_int(interval: int = 0) -> int:
    return int(get_hour(interval))


def wait(i: int = 0):
    time.sleep(i)
