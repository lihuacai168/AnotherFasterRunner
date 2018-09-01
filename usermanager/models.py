from django.db import models


# Create your models here.

class BaseTable(models.Model):
    """
    公共字段列
    """
    class Meta:
        abstract = True
        verbose_name = "公共字段表"
        db_table = 'BaseTable'

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)


class UserInfo(BaseTable):
    """
    用户注册信息表
    """
    class Meta:
        verbose_name = "用户信息"
        db_table = "UserInfo"

    username = models.CharField('用户名', max_length=20, unique=True, null=False)
    password = models.CharField('登陆密码', max_length=100, null=False)
    email = models.EmailField('用户邮箱', unique=True, null=False)


class UserToken(BaseTable):
    """
    用户登陆token
    """
    class Meta:
        verbose_name = "用户登陆token"
        db_table = "UserToken"

    user = models.OneToOneField(to=UserInfo, on_delete=models.CASCADE)
    token = models.CharField('token', max_length=50)


class UserPermission(BaseTable):
    """
    用户权限管理
    """
    class Meta:
        verbose_name = "用户权限管理"
        db_table = "UserPermission"

    permission_union = (
        (1, "admin"),
        (2, "read"),
        (3, "write"),
        (4, "delete")
    )

    user = models.OneToOneField(to=UserInfo, on_delete=models.CASCADE)
    project = models.CharField("项目权限", max_length=50, choices=permission_union)
    api = models.CharField("接口权限", max_length=200, choices=permission_union)
    suite = models.CharField("suite权限", max_length=200, choices=permission_union)
    test = models.CharField("用例权限", max_length=200, choices=permission_union)
    config = models.CharField("配置权限", max_length=200, choices=permission_union)
