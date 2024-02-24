from rest_framework import serializers
from fastuser import models
from django.contrib.auth import get_user_model
User = get_user_model()


class UserInfoSerializer(serializers.Serializer):
    """
    用户信息序列化
    建议实现其他方法，否则会有警告
    """
    username = serializers.CharField(required=True, error_messages={
        "code": "2001",
        "msg": "用户名校验失败"
    })

    password = serializers.CharField(required=True, error_messages={
        "code": "2001",
        "msg": "密码校验失败"
    })

    email = serializers.CharField(required=True, error_messages={
        "code": "2001",
        "msg": "邮箱校验失败"
    })

    def create(self, validated_data):
        """
        实现create方法
        """
        return models.UserInfo.objects.create(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, min_length=6)


class UserModelSerializer(serializers.ModelSerializer):
    """
    访问统计序列化
    """

    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'username', 'is_staff', 'is_active', 'groups']
        depth = 1
