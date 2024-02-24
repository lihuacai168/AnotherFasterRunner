# !/usr/bin/python3

# @Author:梨花菜
# @File: relation.py
# @Time : 2019/5/27 10:16
# @Email: lihuacai168@gmail.com
# @Software: PyCharm
# api模块和数据库api表relation对应关系
API_RELATION = {
    "default": 66,
    "energy.ball": 67,
    "manage": 68,
    "app_manage": 68,
    "artisan": 69,
    "goods": 70,
    "member": 71,
    "order": 72,
    "seller": 73,
    "payment": 74,
    "martketing": 75,
    "promotion": 76,
    "purchase": 77,
    "security": 78,
    "logistics": 79,
    "recycle": 80,
    "image-search": 81,
    "content": 82,
    "bmpm": 83,
    "bi": 84,
}

# Java同学项目分组
API_AUTHOR = {
    "default": 1,
    "tangzhu": 85,
    "xuqirong": 86,
    "zhanghengjian": 87,
    "fengzhenwen": 88,
    "lingyunlong": 89,
    "chencanzhang": 90,
}

NIL = "无参数"
SIGN = "time,rode,sign"
SIGN_OR_TOKEN = SIGN + "(wb-token可选)"
SIGN_AND_TOKEN = SIGN + ",wb-token"
SESSION = "cookie: wb_sess:xxxxxx"
COOKIE = "cookie: wbiao.securityservice.tokenid:xxxx"

API_AUTH = {
    "0": ["NIL", NIL],
    "1": ["APP_GENERAL_AUTH", SIGN],
    "2": ["WXMP_GENERAL_AUTH", SIGN],
    "3": ["APP_MEMBER_AUTH", SIGN_AND_TOKEN],
    "4": ["APP_MEMBER_COMPATIBILITY_AUTH", SIGN_OR_TOKEN],
    "5": ["WXMP_MEMBER_AUTH", SIGN_AND_TOKEN],
    "6": ["WXMP_MEMBER_COMPATIBILITY_AUTH", SIGN_OR_TOKEN],
    "7": ["APP_USER_AUTH", SIGN_AND_TOKEN],
    "8": ["APP_USER_COMPATIBILITY_AUTH", SIGN_OR_TOKEN],
    "9": ["WXMP_USER_AUTH", SIGN_AND_TOKEN],
    "10": ["WXMP_USER_COMPATIBILITY_AUTH", SIGN_OR_TOKEN],
    "11": ["WXMP_MEMBER_COMPATIBILITY_AUTH", SESSION],
    "12": ["PM_USER_AUTH", COOKIE],
    "13": ["BACK_USER_AUTH", COOKIE],
    "14": ["APP_NIL", NIL],
    "15": ["WXMP_NIL", NIL],
    "16": ["PM_NIL", NIL],
}
