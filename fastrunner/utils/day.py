# !/usr/bin/python3

# @Author: 花菜
# @File: day.py
# @Time : 2020/11/4 14:53
# @Email: lihuacai168@gmail.com
import datetime

from httprunner.builtin import get_ts_int


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
    time_str = "%Y-%m-%d"
    if kwargs:
        h = kwargs.get("h", "00")
        m = kwargs.get("m", "00")
        s = kwargs.get("s", "00")
        time_str = f"{time_str} {h}:{m}:{s}"
    return (n + d).strftime(time_str)


def get_week(weeks: int = 0):
    """生成一年中的第n周"""
    week_delta = 7 * 24 * 60 * 60 * weeks
    ts = get_ts_int(week_delta)
    dt = datetime.datetime.fromtimestamp(ts)
    year, week_number, _ = dt.isocalendar()
    # '202133' 2021年的第33周
    return f"{year}{week_number}"


def get_month(month_delta: int = 0, base_ts=get_ts_int):
    """生成年月
    # 1629439316 对应的日期2021年08月20日
    >>> base_ts = 1629439316
    >>> get_month(5, base_ts)
    '202201'

    >>> get_month(17, base_ts)
    '202301'

    >>> get_month(-20, base_ts)
    '201912'

    >>> get_month(-8, base_ts)
    '202012'

    >>> get_month(base_ts=base_ts)
    '202108'

    >>> get_month(1, base_ts)
    '202109'

    >>> get_month(-1, base_ts)
    '202107'
    """
    if callable(base_ts):
        base_ts = base_ts()
    dt = datetime.datetime.fromtimestamp(base_ts)
    year, month = dt.year, dt.month

    # 超过12个月，先计算年份，然后再对月份差取余
    if abs(month_delta) > 12:
        year_delta = abs(month_delta) // 12
        if month_delta > 0:
            year += year_delta
            month_delta = month_delta % 12
        else:
            year -= year_delta
            month_delta = -(abs(month_delta) % 12)

    # 月份差是正数，有两种情况
    # 1.月份差和当前的月份相加 > 12, 年份+1, 月份等于超过的减去12
    # 2.月份差和当前月份相加 <= 12, 直接相加
    if month_delta >= 0:
        if month + month_delta > 12:
            year += 1
            month = month + month_delta - 12
        else:
            month += month_delta
    else:
        # 月份差是负数, 有两种情况
        # 1.月份差 <= 0, 年份-1，月份从12开始倒退
        # 2.直接倒退月份
        if month - abs(month_delta) <= 0:
            year -= 1
            # month + month_delta 是负数
            month = 12 + (month + month_delta)
        else:
            month += month_delta
    month = str(month).rjust(2, "0")

    return f"{year}{month}"


def get_month_format(month_delta: int = 0, base_ts=get_ts_int):
    month = get_month(month_delta, base_ts)
    return f"{month[:4]}年{month[4:]}月"


def get_week_format(weeks):
    week = get_week(weeks)
    return f"{week[:4]}年{week[4:]}周"


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
