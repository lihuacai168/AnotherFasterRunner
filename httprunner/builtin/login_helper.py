# !/usr/bin/python3

# @Author: 花菜
# @File: login_helper.py
# @Time : 2021/8/9 17:30
# @Email: lihuacai168@gmail.com
import json
import logging

import pydash
import requests

# from loguru import logger

uac_token_url = "http://192.168.22.19:8002/api/uac/token/"

logger = logging.getLogger("httprunner")


def _get_token(biz, account, password, env="qa"):
    data = {"biz": biz, "account": account, "password": password, "env": env}
    headers = {"Content-Type": "application/json; charset=utf-8"}
    res = requests.post(url=uac_token_url, headers=headers, data=json.dumps(data)).json()
    return res, data


def get_userid(biz, account, password, env="qa"):
    res, data = _get_token(biz, account, password, env)
    user_id = pydash.get(res, "user_id")
    if user_id:
        logger.info(f"获取user_id成功: {user_id}")
        return user_id
    else:
        logger.warning(f"获取user_id失败，入参是: {data}, 响应是: {res}")
        raise Exception("获取user_id失败")


def get_uac_token(biz, account, password, env="qa"):
    res, data = _get_token(biz, account, password, env)
    token = pydash.get(res, "token")
    if token:
        logger.info(f"获取token成功: {token}")
        return token
    else:
        logger.warning(f"获取token失败，入参是: {data}, 响应是: {res}")
        raise Exception("获取token失败")


if __name__ == "__main__":
    get_userid("cm", "13533975028", "397726")
    get_uac_token("cm", "13533975028", "397726")
