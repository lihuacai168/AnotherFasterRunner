# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: time_helper.py
# @Time : 2021/7/26 18:26
# @Email: lihuacai168@gmail.com

import datetime
import time


def get_day(days: int = 0, **kwargs):
    """获取日期，无连接符格式
    days : int
        负数表示过去， 正数表示未来
    kwargs : str, 可选h, m, s
        h : 第n小时
        m : 第n分钟
        s : 第n秒

    >>> get_day()
    20201015 # 今天的日期

    >>> get_day(1)
    20201016 # 明天的日期

    >>> get_day(-1)
    20201014 # 昨天的日期

    >>> get_day(h=9,m=15,s=30)
    20210807 9:15:30 # 今天的9时15分30秒

    >>> get_day(sep='-', h=9,m=15,s=30)
    2021-08-07 9:15:30 # 今天的9时15分30秒, 日期分隔符是-
    """
    d = datetime.timedelta(days)
    n = datetime.datetime.now()
    sep: str = kwargs.get("sep", "")
    fmt = sep.join(["%Y", "%m", "%d"])
    if kwargs:
        h = kwargs.get("h", "00")
        m = kwargs.get("m", "00")
        s = kwargs.get("s", "00")
        fmt = f"{fmt} {h}:{m}:{s}"
    return (n + d).strftime(fmt)


def get_day_fmt(fmt_type="sec", **kwargs):
    """获取日期

    fmt_type : str
        日期格式，默认'sec', 包含时分秒, 'day'只包含年月日
    kwargs : str, key可以是days, hours, seconds, 等
        时间差值，负数表示过去，正数表示未来
        昨天：days=-1，明天days=1

    >>> get_day_fmt()
    # 当前日期，包含时分秒
    2021-08-07 12:08:54

    >>> get_day_fmt('day')
    # 当前日期，只包含年月日
    2021-08-07

    # 昨天的日期
    >>> get_day_fmt('day', days=-1)
    2021-08-06
    """
    fmt = "%Y-%m-%d %H:%m:%S"
    if fmt_type == "day":
        fmt = "%Y-%m-%d"

    day = datetime.timedelta(**kwargs)
    now = datetime.datetime.now()
    return (now + day).strftime(fmt)


def get_day_h(days: int = 0, **kwargs):
    """
    >>> get_day_h(0,h=7)
    2021042207
    """
    d = datetime.timedelta(days)
    n = datetime.datetime.now()
    time_str = "%Y%m%d"
    if kwargs:
        h = str(kwargs.get("h"))
        h = h.rjust(2, "0")
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
        return str(int(time.mktime(time_arr)))


def get_ts_int(interval: int = 0, t=None) -> int:
    return int(get_ts(interval, t))


def get_hour_ts(interval: int = 0) -> str:
    # 当前时间所在的小时，转换为时间戳
    # 2021-3-9 17:0:12, 取2021-3-9 17:0:0，然后转换为时间戳
    now_hour = int(
        datetime.datetime.now()
        .replace(minute=0, second=0, microsecond=0)
        .timestamp()
    )
    return str(now_hour + interval * 3600)


def get_hour() -> str:
    # 获取当前的小时，不足两位补0
    return str(datetime.datetime.now().hour).rjust(2, "0")


def get_hour_ts_int(interval: int = 0) -> int:
    return int(get_hour(interval))


def wait(i: int = 0):
    time.sleep(i)
