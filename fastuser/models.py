from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class BaseTable(models.Model):
    """
    公共字段列
    """

    class Meta:
        abstract = True
        verbose_name = "公共字段表"
        db_table = 'base_table'

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    creator = models.CharField(verbose_name="创建人", max_length=20, null=True)
    updater = models.CharField(verbose_name="更新人", max_length=20, null=True)


class UserInfo(BaseTable):
    """
    用户注册信息表
    """

    class Meta:
        verbose_name = "用户信息"
        db_table = "user_info"

    level_type = (
        (0, '普通用户'),
        (1, '管理员'),
    )
    username = models.CharField('用户名', max_length=20, unique=True, null=False)
    password = models.CharField('登陆密码', max_length=100, null=False)
    email = models.EmailField('用户邮箱', unique=True, null=False)
    level = models.IntegerField('用户等级', choices=level_type, default=0)


class UserToken(BaseTable):
    """
    用户登陆token
    """

    class Meta:
        verbose_name = "用户登陆token"
        db_table = "user_token"

    user = models.OneToOneField(to=UserInfo, on_delete=models.CASCADE, db_constraint=False)
    token = models.CharField('token', max_length=50)


class MyUser(AbstractUser):
    phone = models.CharField(verbose_name='手机号码', unique=True, null=False, max_length=11)

    class Meta(AbstractUser.Meta):
        pass
