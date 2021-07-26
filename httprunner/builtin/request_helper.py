# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: request_helper.py
# @Time : 2021/7/26 18:33
# @Email: lihuacai168@gmail.com

import json

import pydash
from loguru import logger


def set_json(request_obj, in_data={}, include="", json_path="."):
    """
    修改请求体的json
    """
    if isinstance(in_data, (dict, list)) is False:
        try:
            in_data = json.loads(in_data)
        except Exception as e:
            logger.error(str(e))
            raise e
    request_data = pydash.get(request_obj['json'], json_path)
    include_key = include.split("-")
    for k in include_key:
        v = pydash.get(in_data, k)
        path = k.split('.')[-1]
        pydash.set_(request_data, path, v)
