# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: comparators.py
# @Time : 2021/7/26 18:08
# @Email: lihuacai168@gmail.com

# encoding: utf-8

"""
Built-in dependent functions used in YAML/JSON testcases.
"""

import re

import pydash

from httprunner.compat import basestring, builtin_str, integer_types

"""
built-in comparators
"""


def equals(check_value, expect_value):
    assert check_value == expect_value


def less_than(check_value, expect_value):
    assert check_value < expect_value


def less_than_or_equals(check_value, expect_value):
    assert check_value <= expect_value


def greater_than(check_value, expect_value):
    assert check_value > expect_value


def greater_than_or_equals(check_value, expect_value):
    assert check_value >= expect_value


def not_equals(check_value, expect_value):
    assert check_value != expect_value


def string_equals(check_value, expect_value):
    assert builtin_str(check_value) == builtin_str(expect_value)


def length_equals(check_value, expect_value):
    assert isinstance(expect_value, integer_types)
    assert len(check_value) == expect_value


def length_greater_than(check_value, expect_value):
    assert isinstance(expect_value, integer_types)
    assert len(check_value) > expect_value


def length_greater_than_or_equals(check_value, expect_value):
    assert isinstance(expect_value, integer_types)
    assert len(check_value) >= expect_value


def length_less_than(check_value, expect_value):
    assert isinstance(expect_value, integer_types)
    assert len(check_value) < expect_value


def length_less_than_or_equals(check_value, expect_value):
    assert isinstance(expect_value, integer_types)
    assert len(check_value) <= expect_value


def contains(check_value, expect_value):
    assert isinstance(check_value, (list, tuple, dict, basestring))
    assert expect_value in check_value


def not_contains(check_value, expect_value):
    assert isinstance(check_value, (list, tuple, dict, basestring))
    assert check_value not in expect_value


def contained_by(check_value, expect_value):
    assert isinstance(expect_value, (list, tuple, dict, basestring))
    assert check_value in expect_value


def _get_expression(item, expression, expect_value, jsonpath):
    parsed_expression = None
    if isinstance(item, dict):
        item_value = pydash.get(item, jsonpath)

        if isinstance(item_value, (int, float, list, dict, bool, type(None))):
            parsed_expression = f"{item_value} {expression} {expect_value}"
        else:
            parsed_expression = f"'{pydash.get(item, jsonpath)}' {expression} '{expect_value}'"

    if isinstance(item, str):
        parsed_expression = f"{item} {expression} {expect_value}"

    if parsed_expression is None:
        raise AssertionError("list的元素只能是dict或者string")

    return parsed_expression


def list_any_item_contains(check_value: list, jsonpath_expression_value):
    assert isinstance(check_value, list)
    jsonpath, expression, expect_value = jsonpath_expression_value.split(" ")
    for item in check_value:
        parsed_expression = _get_expression(
            item=item, expression=expression, expect_value=expect_value, jsonpath=jsonpath
        )
        try:
            if eval(parsed_expression) is True:
                break
        except Exception as e:
            raise e
    else:
        raise AssertionError(f"{check_value} {expression} {expect_value}")


def list_all_item_contains(check_value: list, jsonpath_expression_value):
    assert isinstance(check_value, list)
    jsonpath, expression, expect_value = jsonpath_expression_value.split(" ")
    for item in check_value:
        parsed_expression = _get_expression(
            item=item, expression=expression, expect_value=expect_value, jsonpath=jsonpath
        )
        try:
            if eval(parsed_expression) is False:
                raise AssertionError(f"{check_value} {expression} {expect_value}")
        except Exception as e:
            raise e


def type_match(check_value, expect_value):
    def get_type(name):
        if isinstance(name, type):
            return name
        elif isinstance(name, basestring):
            try:
                return __builtins__[name]
            except KeyError:
                raise ValueError(name)
        else:
            raise ValueError(name)

    assert isinstance(check_value, get_type(expect_value))


def regex_match(check_value, expect_value):
    assert isinstance(expect_value, basestring)
    assert isinstance(check_value, basestring)
    assert re.match(expect_value, check_value)


def startswith(check_value, expect_value):
    assert builtin_str(check_value).startswith(builtin_str(expect_value))


def endswith(check_value, expect_value):
    assert builtin_str(check_value).endswith(builtin_str(expect_value))
