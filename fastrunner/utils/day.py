# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: day.py
# @Time : 2020/11/4 14:53
# @Email: lihuacai168@gmail.com
import datetime


def get_day(days: int = 0, **kwargs):
    """
    >>> get_day()
    2020-10-15 # 今天的日期

    >>> get_day(1)
    2020-10-16 # 明天的日期

    >>> get_day(-1)
    2020-10-14 # 昨天的日期
    """
    d = datetime.timedelta(days)
    n = datetime.datetime.now()
    time_str = f"%Y-%m-%d"
    if kwargs:
        h = kwargs.get("h", "00")
        m = kwargs.get("m", "00")
        s = kwargs.get("s", "00")
        time_str = f"{time_str} {h}:{m}:{s}"
    return (n + d).strftime(time_str)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
