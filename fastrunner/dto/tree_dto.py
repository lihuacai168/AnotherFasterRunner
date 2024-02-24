# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: tree_dto.py
# @Time : 2022/9/4 19:05
# @Email: lihuacai168@gmail.com

from pydantic import BaseModel, Field


class TreeUniqueIn(BaseModel):
    project_id: int
    type: int


class TreeUpdateIn(BaseModel):
    tree: list[dict] = Field(alias="body")


class TreeOut(BaseModel):
    tree: list[dict]
    id: int
    max: int
