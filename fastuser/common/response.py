KEY_MISS = {"code": "0100", "success": False, "msg": "请求数据非法"}

REGISTER_USERNAME_EXIST = {"code": "0101", "success": False, "msg": "用户名已被注册"}

REGISTER_EMAIL_EXIST = {"code": "0101", "success": False, "msg": "邮箱已被注册"}

SYSTEM_ERROR = {"code": "9999", "success": False, "msg": "System Error"}

REGISTER_SUCCESS = {"code": "0001", "success": True, "msg": "register success"}

LOGIN_FAILED = {"code": "0103", "success": False, "msg": "用户名或密码错误"}

USER_NOT_EXISTS = {"code": "0104", "success": False, "msg": "该用户未注册"}

USER_BLOCKED = {"code": "0105", "success": False, "msg": "用户被禁用"}

LOGIN_SUCCESS = {"code": "0001", "success": True, "msg": "login success"}
