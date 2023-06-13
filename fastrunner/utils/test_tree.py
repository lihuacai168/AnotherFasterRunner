# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: test_tree.py
# @Time : 2020/1/3 1:13
# @Email: lihuacai168@gmail.com
# @Software: PyCharm
from unittest import TestCase
from .tree import get_tree_label, get_all_ycatid, get_faster_id_by_ycatid, get_tree_ycatid_mapping,\
    get_tree_relation_name, get_tree_max_id, get_tree_max_id_old


class Test(TestCase):
    tree = [
        {'id': 1, 'label': '默认分组', 'children': []},
        {'id': 2, 'label': '不带token', 'children': [
            {'id': 3, 'label': '杂志', 'children': [dict(id=323, label='个人中心', children=[])]},
            {'id': 4, 'label': '我的页面', 'children': []},
            {'id': 5, 'label': '购物车', 'children': []},
            {'id': 6, 'label': '选表', 'children': []},
            {'id': 7, 'label': '店铺', 'children': []},
            {'id': 11, 'label': '首页', 'children': []},
            {'id': 13, 'label': '商品详情', 'children': []},
            {'id': 15, 'label': '启动页', 'children': []}
        ]},
        {'id': 30, 'label': 'M站', 'children': []},
        {'id': 34, 'label': '注册', 'children': []}
    ]

    def test_get_tree_max_id(self):
        assert get_tree_max_id(self.tree) == 323

    def test_get_tree_max_id_old(self):
        assert get_tree_max_id_old(self.tree) == 323

    def test_get_tree_max_id_empty(self):
        assert get_tree_max_id([]) == 0

    def test_get_tree_label_default(self):
        assert get_tree_label(self.tree, '默认分组') == 1

    def test_get_tree_label(self):
        assert get_tree_label(self, search_label='tree为空') == 1

    def test_get_tree_label_children(self):
        assert get_tree_label(self.tree, '杂志') == 3

    def test_get_tree_label_second_children(self):
        assert get_tree_label(self.tree, '个人中心') == 323

    def test_get_tree_relation_name_default(self):
        assert get_tree_relation_name(self.tree, 1) == '默认分组'

    def test_get_tree_relation_name_index(self):
        assert get_tree_relation_name(self.tree, 11) == '首页'


class TestYAPITree(TestCase):
    tree = [
        {'id': 1, 'yapi_catid': 100, 'label': '测试分组1', 'children': [
            {'id': 2, 'yapi_catid': 101, 'label': '聚合数据', 'children': []},
            {'id': 3, 'label': 'eee', 'children': []}
        ]},
        {'id': 30, 'yapi_catid': 102, 'label': '222', 'children': []}
    ]

    def test_get_all_ycatid_default(self):
        assert get_all_ycatid(self.tree) == [100, 101, 102]

    def test_get_all_ycatid_empty(self):
        assert get_all_ycatid([]) == []

    def test_get_faster_id_by_ycatid_default(self):
        assert get_faster_id_by_ycatid(self.tree, 102) == 30

    def test_get_faster_id_by_ycatid_not_found(self):
        assert get_faster_id_by_ycatid(self.tree, 103) == 0

    def test_get_faster_id_by_ycatid_mapping_deleted(self):
        assert get_tree_ycatid_mapping(self.tree) == {100: 1, 101: 2, 102: 30}
