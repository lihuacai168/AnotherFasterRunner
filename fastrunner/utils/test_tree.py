# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: test_tree.py 
# @Time : 2020/1/3 1:13
# @Email: lihuacai168@gmail.com
# @Software: PyCharm
from unittest import TestCase
from .tree import get_tree_label


class Test(TestCase):
    tree = [{'id': 1, 'label': '默认分组', 'children': []},
            {'id': 2, 'label': '不带token', 'children': [{'id': 3, 'label': '杂志', 'children': [
                dict(id=323, label='个人中心', children=[])]},
                                                       {'id': 4, 'label': '我的页面', 'children': []},
                                                       {'id': 5, 'label': '购物车', 'children': []},
                                                       {'id': 6, 'label': '选表', 'children': []},
                                                       {'id': 7, 'label': '店铺', 'children': []},
                                                       {'id': 11, 'label': '首页', 'children': []},
                                                       {'id': 13, 'label': '商品详情', 'children': []},
                                                       {'id': 15, 'label': '启动页', 'children': []}]},
            {'id': 30, 'label': 'M站', 'children': []}, {'id': 34, 'label': '注册', 'children': []}]

    def test_get_tree_label_default(self):
        assert get_tree_label(self.tree, '默认分组') == 1

    def test_get_tree_label(self):
        assert get_tree_label(self, search_label='tree为空') == 1

    def test_get_tree_label_children(self):
        assert get_tree_label(self.tree, '杂志') == 3

    def test_get_tree_label_second_children(self):
        assert get_tree_label(self.tree, '个人中心') == 323
