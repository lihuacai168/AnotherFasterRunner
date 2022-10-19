from django.db import models
from django.utils import timezone


class TyAdminSysLog(models.Model):
    action_time = models.DateTimeField(verbose_name="动作时间", default=timezone.now)
    ip_addr = models.CharField(max_length=39, blank=True, null=True, verbose_name="操作ip")
    action_flag = models.CharField(blank=True, null=True, max_length=32, verbose_name="操作flag")
    message = models.TextField(verbose_name="日志记录")
    log_type = models.CharField(default="", max_length=200, verbose_name="日志类型")
    user_name = models.CharField(max_length=200, default="1", verbose_name="用户")

    class Meta:
        verbose_name = "系统日志"
        verbose_name_plural = verbose_name
        ordering = ('-action_time',)


class TyAdminEmailVerifyRecord(models.Model):
    """邮箱验证码model"""
    SEND_CHOICES = (
        ("register", "注册"),
        ("forget", "找回密码"),
        ("update_email", "修改邮箱"),
        ("login_auth", "登录授权"),
    )
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(choices=SEND_CHOICES, max_length=20, verbose_name="验证码类型")
    send_time = models.DateTimeField(default=timezone.now, verbose_name=u"发送时间")

    class Meta:
        verbose_name = "TyAdmin邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)
