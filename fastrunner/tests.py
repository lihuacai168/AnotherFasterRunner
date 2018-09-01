import json
from collections import OrderedDict

from django.test import TestCase
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FasterRunner.settings")  # project_name 项目名称
django.setup()

from fastrunner import models

models.DataBase.objects.create(**{
    "type": 1,
    "name": "1",
    "server": "1",
    "account": "1",
    "password": "1",
    "desc": "1"
})


def get_tree():
    querset = models.Relation.objects

    parent_tree = [{"id": v.node_id, "label": v.label, "children": []} for v in querset.filter(tag=1)]
    child_tree = [{"id": v.node_id, "label": v.label, "children": []} for v in querset.exclude(tag=1)]


def iterable_node(parent_tree, child_tree):
    for v in child_tree:
        pass


c = []


def get_max_id(value):
    if isinstance(value, dict):
        c.append(value['id'])
        if len(value['children']) != 0:
            get_max_id(value['children'])

    if isinstance(value, list):
        for v in value:
            if len(v['children']) != 0:
                get_max_id(v['id'])


def list_all_dict(dict_a):
    if isinstance(dict_a, dict):  # 使用isinstance检测数据类型

        for x in range(len(dict_a)):
            temp_key = dict_a.keys()[x]

            temp_value = dict_a[temp_key]

            print(temp_key, temp_value)

            list_all_dict(temp_value)  # 自我调用实现无限遍历


def file_iterator(file_name, chunk_size=512):
    """
    读取文件 yield生成器
    """
    with open(file_name, 'rb') as f:
        while True:
            content = f.read(chunk_size)
            if content:
                yield content
            else:
                break


def read_file_rb(file_path):
    with open(file_path, 'rb') as stream:
        return stream.read()


if __name__ == '__main__':

    pass

