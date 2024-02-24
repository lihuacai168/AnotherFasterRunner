# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: 花菜
# @File: crud_helper.py
# @Time : 2022/9/4 17:59
# @Email: lihuacai168@gmail.com

import traceback
from typing import TypeVar

from loguru import logger

from fastrunner.models import BaseTable

BModel = TypeVar("BModel", bound=BaseTable)


def create(creator: str, model: BModel, payload: dict) -> int:
    try:
        logger.info(f"input: create={model.__name__}, payload={payload}")
        obj = model.objects.create(creator=creator, **payload)
    except Exception as e:
        logger.warning(traceback.format_exc())
        raise e
    logger.info(f"create {model.__name__} success, id: {obj.id}")


def get_or_create(model: BModel, filter_kwargs: dict, defaults: dict) -> tuple["obj", bool]:
    """
    :raises DoesNotExist
    """
    logger.info(f"input: get_or_create={model.__name__}, filter_kwargs={filter_kwargs}, defaults={defaults}")
    obj, created = model.objects.get_or_create(
        defaults=defaults,
        **filter_kwargs,
    )
    return obj, created


def update(
    obj,
    updater: str,
    payload: dict,
) -> int:
    logger.info(f"input: update model={obj.__class__.__name__}, id={obj.id}, payload={payload}")
    if updater:
        obj.updater = updater
    for attr, value in payload.items():
        if hasattr(obj, attr) is False:
            logger.warning(f"{attr=} not in obj fields, it will not update")
        setattr(obj, attr, value)
    try:
        obj.save()
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e
    logger.info(f"update {obj.__class__.__name__} success, id: {obj.id}")
    return obj.id
