# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: 花菜
# @File: tree_service_impl.py
# @Time : 2022/9/4 18:57
# @Email: lihuacai168@gmail.com

import traceback
from typing import Union

from loguru import logger

from curd.base_curd import GenericCURD
from fastrunner.dto.tree_dto import TreeOut, TreeUniqueIn, TreeUpdateIn
from fastrunner.models import Relation
from fastrunner.utils.response import (
    TREE_ADD_SUCCESS,
    TREE_UPDATE_SUCCESS,
    StandResponse,
)
from fastrunner.utils.tree import get_tree_max_id


class TreeService:
    def __init__(self):
        self.model = Relation
        self.curd = GenericCURD(self.model)

    def get_or_create(self, query: TreeUniqueIn) -> StandResponse[TreeOut]:
        default_tree: list = [
            {"id": 1, "label": "default node", "children": []}
        ]
        tree_obj, created = self.curd.get_or_create(
            filter_kwargs=query.dict(),
            defaults={"tree": default_tree, "project_id": query.project_id},
        )
        if created:
            logger.info(f"tree created {query=}")
            body: list[dict] = tree_obj.tree
        else:
            logger.info(f"tree exist {query=}")
            body: list[dict] = eval(tree_obj.tree)
        tree = {
            "tree": body,
            "id": tree_obj.id,
            "success": True,
            "max": get_tree_max_id(body),
        }
        return StandResponse[TreeOut](**TREE_ADD_SUCCESS, data=TreeOut(**tree))

    def patch(
        self, pk: int, payload: TreeUpdateIn
    ) -> StandResponse[Union[TreeOut, None]]:
        try:
            pk: int = self.curd.update_obj_by_pk(pk, None, payload.dict())
        except Exception:
            err: str = traceback.format_exc()
            logger.warning(f"update tree {err=}")
            return StandResponse[None](
                code="9999", success=False, msg=err, data=None
            )
        return StandResponse[TreeOut](
            **TREE_UPDATE_SUCCESS,
            data=TreeOut(
                tree=payload.tree, id=pk, max=get_tree_max_id(payload.tree)
            ),
        )


tree_service = TreeService()
