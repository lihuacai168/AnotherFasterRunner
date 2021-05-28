# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: schema.py
# @Time : 2021/5/28 11:26
# @Email: lihuacai168@gmail.com
import json5


def load_json_from_string(s: str) -> dict:
    try:
        json_data = json5.loads(s, encoding='utf-8')
    except Exception as e:
        raise ValueError(f"JSON loads errors: {e}")
    else:
        return json_data


def schema2json(schema: dict, res_json: dict = {}):
    """
    递归遍历schema

    有三种情况
    1. type: 不是object和array, 直接赋值
    2. type:object, 遍历properties
    3. type:array, 遍历items?
    """
    value_type: str = schema['type']
    if value_type == 'object':
        properties = schema.get('properties', {})
        for k, v in properties.items():
            value_type = v['type']
            if value_type == 'object':
                obj = schema2json(v, {})
                res_json.update({k: obj})
            elif value_type == 'array':
                items: dict = v['items']
                if items['type'] == 'object':
                    obj = schema2json(items, {})
                    res_json.update({k: [obj]})
                elif items['type'] == 'array':
                    # TODO 列表嵌套列表
                    pass
                else:
                    res_json.update({k: []})
            else:
                res_json[k] = f'${k}'
    return res_json



