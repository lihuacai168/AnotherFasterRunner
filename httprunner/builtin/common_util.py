# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: common_util.py
# @Time : 2021/7/26 18:10
# @Email: lihuacai168@gmail.com
import datetime
import os
import random
import string
import time

from loguru import logger
from requests_toolbelt import MultipartEncoder

from httprunner.compat import builtin_str, integer_types
from httprunner.exceptions import ParamsError


def gen_random_string(str_len):
    """ generate random string with specified length
    """
    return ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(str_len))


def get_timestamp(str_len=13):
    """ get timestamp string, length can only between 0 and 16
    """
    if isinstance(str_len, integer_types) and 0 < str_len < 17:
        return builtin_str(time.time()).replace(".", "")[:str_len]

    raise ParamsError("timestamp length can only between 0 and 16.")


def get_current_date(fmt="%Y-%m-%d"):
    """ get current date, default format is %Y-%m-%d
    """
    return datetime.datetime.now().strftime(fmt)


def multipart_encoder(field_name, file_path, file_type=None, file_headers=None):
    if not os.path.isabs(file_path):
        file_path = os.path.join(os.getcwd(), file_path)

    filename = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        fields = {
            field_name: (filename, f.read(), file_type)
        }

    return MultipartEncoder(fields)


def multipart_content_type(multipart_encoder):
    return multipart_encoder.content_type


""" built-in hooks
"""


def setup_hook_prepare_kwargs(request):
    pass
