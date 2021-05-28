# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: test_schema.py
# @Time : 2021/5/28 12:47
import json
from unittest import TestCase
from .schema import schema2json
from genson import SchemaBuilder


class Test(TestCase):
    def test_schema2json_basic(self):
        d = {'k': '$k', 'k2': '$k2'}
        builder = SchemaBuilder()
        builder.add_object(d)
        dict_schema = builder.to_schema()

        res = schema2json(dict_schema)
        assert d == res

    def test_schema2json_nested_dict(self):
        d = {'k': '$k', 'd1': {"k1": "$k1", "k2": "$k2"}}
        builder = SchemaBuilder()
        builder.add_object(d)
        dict_schema = builder.to_schema()

        res = schema2json(dict_schema)
        assert d == res

    def test_schema2json_list(self):
        d = {'k': '', 'l': [{"k": "", "k2": ""}, {"k": "", "k2": ""}]}
        builder = SchemaBuilder()
        builder.add_object(d)
        dict_schema = builder.to_schema()

        res = schema2json(dict_schema)
        assert res == {'k': '$k', 'l': [{"k": "$k", "k2": "$k2"}]}

    def test_schema2json_list(self):
        d = {'k': '', 'l': [{"k": "", "k2": ""}, {
            "k": "", "k2": ""}], 'k3': '', 'k4': {"k5": ""}}
        builder = SchemaBuilder()
        builder.add_object(d)
        dict_schema = builder.to_schema()

        res = schema2json(dict_schema)
        assert res == {'k': '$k', 'l': [
            {"k": "$k", "k2": "$k2"}], 'k3': "$k3", 'k4': {"k5": "$k5"}}

    def test_schema2json_list_dict_dict(self):
        d = {'k': '', 'l': [{"k": "", "k2": "", "d1": {"k": "", "k2": ""}}]}
        builder = SchemaBuilder()
        builder.add_object(d)
        dict_schema = builder.to_schema()

        res = schema2json(dict_schema)
        assert res == {'k': '$k', 'l': [
            {"k": "$k", "k2": "$k2", "d1": {"k": "$k", "k2": "$k2"}}]}
