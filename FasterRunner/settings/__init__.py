# !/usr/bin/python3

# @Author:梨花菜
# @File: __init__.py.py
# @Time : 2019/6/14 17:05
# @Email: lihuacai168@gmail.com
# @Software: PyCharm

# 兼容已经移除的方法
import django
from django.utils.encoding import smart_str

django.utils.encoding.smart_text = smart_str

from django.utils.translation import gettext_lazy

django.utils.translation.ugettext = gettext_lazy
django.utils.translation.ugettext_lazy = gettext_lazy
