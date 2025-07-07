# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author:梨花菜
# @File: test.py
# @Time : 2019/6/13 11:53
# @Email: lihuacai168@gmail.com
# @Software: PyCharm

from django.test import TestCase
from django.utils.crypto import get_random_string

from fastuser import models


class ModelTest(TestCase):
    def setUp(self):
        """
        注册:{
            "username": "demo"
            "password": "1321"
            "email": "1@1.com"
        }
        """
        models.UserInfo.objects.create(
            username="rikasai", password=get_random_string(32), email="lihuacai168@gmail.com"
        )

    def test_user_register(self):
        res = models.UserInfo.objects.get(username="rikasai")
        self.assertEqual(res.email, "lihuacai168@gmail.com")
