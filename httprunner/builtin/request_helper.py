# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: request_helper.py
# @Time : 2021/7/26 18:33
# @Email: lihuacai168@gmail.com

import json
import logging

import pydash

# from loguru import logger

logger = logging.getLogger("httprunner")


def _load_json(in_data):
    if isinstance(in_data, (dict, list)) is False:
        try:
            in_data = json.loads(in_data)
        except Exception as e:
            logger.error(str(e))
            raise e
    return in_data


def set_json(request_obj, in_data={}, include="", json_path="."):
    """
    修改请求体的json, 包含模式
    """
    in_data = _load_json(in_data)
    request_data = pydash.get(request_obj["json"], json_path)
    include_keys = include.split("-")
    for k in include_keys:
        v = pydash.get(in_data, k)
        path = k.split(".")[-1]
        pydash.set_(request_data, path, v)


def set_json_e(request_obj, in_data={}, exclude="", in_path="."):
    """
    修改请求体的json， 排除模式
    """
    in_data = _load_json(in_data)
    request_data = pydash.get(request_obj["json"], in_path)
    exclude_keys = exclude.split("-")
    if isinstance(in_data, dict):
        for k, v in in_data.items():
            if k in exclude_keys:
                continue
            pydash.set_(request_data, k, v)
    else:
        for index, value in enumerate(in_data):
            if index in exclude_keys:
                continue
            pydash.set_(request_data, index, value)
