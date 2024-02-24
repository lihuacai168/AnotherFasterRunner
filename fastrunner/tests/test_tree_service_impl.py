# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: 花菜
# @File: test_tree_service_impl.py
# @Time : 2022/9/5 00:22
# @Email: lihuacai168@gmail.com


from django.test import TestCase

from fastrunner.dto.tree_dto import TreeUniqueIn, TreeUpdateIn
from fastrunner.services.tree_service_impl import tree_service


class TestTreeServiceImpl(TestCase):
    default_tree: list[dict] = [
        {"id": 1, "label": "default node", "children": []}
    ]
    service = tree_service

    def test_get_or_create(self):
        assert (
            self.service.get_or_create(
                TreeUniqueIn(project_id=100, type=1)
            ).data.tree
            == self.default_tree
        )

        assert (
            # cover exist case
            self.service.get_or_create(
                TreeUniqueIn(project_id=100, type=1)
            ).data.tree
            == self.default_tree
        )

    def test_patch(self):
        input_body: list[dict] = [
            {
                "id": 1,
                "label": "default node",
                "children": [{"id": 2, "label": "sub", "children": []}],
            }
        ]
        pk: int = self.service.get_or_create(
            TreeUniqueIn(project_id=101, type=1)
        ).data.id

        self.service.patch(pk=pk, payload=TreeUpdateIn(body=input_body))
        assert (
            self.service.get_or_create(
                TreeUniqueIn(project_id=101, type=1)
            ).data.tree
            == input_body
        )

        assert (
            self.service.patch(
                pk=999,
                payload=TreeUpdateIn(body=input_body),  # pk not exist
            ).data
            is None
        )
