# -*- coding:utf-8 -*-
# @Time   :2022/3/26 9:45
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :auth.py
from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from sqtp.models import User


# 用户序列化器
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['date_joined', 'email', 'id', 'is_active',
                  'is_superuser', 'phone', 'realname', 'username','user_type']


# 注册用户序列化器
class RegisterSerializer(serializers.ModelSerializer):
    admin_code = serializers.CharField(default='')  # 在序列化器里面注册字段使用serializers.类型就可以创建

    # 创建元类，指定接收的字段
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone', 'realname', 'admin_code']

    # 自定义校验器（这里使用validate）
    def validate(self, attrs):  # attr是一字典的形式传进来的
        # 校验admin_code是否正确，正确就直接返回
        if attrs.get('admin_code') and attrs['admin_code'] != 'sqtp':
            raise ValidationError('错误的admin_code')  # 使用DRF框架自带的捕获错误信息的内容
        return attrs

    # 重写序列化器保存方法
    def register(self):
        # 获取入参
        # 这里的data就是校验器里面校验之后的data数据
        in_param = self.data
        if 'admin_code' in in_param:  # 如果入参里面有admin_code，就创建超级管理员
            in_param.pop('admin_code')  # 因为用户模型表没有该字段，传入会报错，所以确定有admin_code就先删除在创建
            user = User.objects.create_superuser(**in_param)  # create_superuser是DRF自带的创建超级管理员方法
        else:
            user = User.objects.create_user(**in_param)  # create_user 是DRF自带的创建的普通管理员方法
        return user


# 登录序列化器
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, attrs):
        # 验证用户名和密码
        user = auth.authenticate(**attrs)
        if not user:
            raise ValidationError('用户名或密码错误')
        return user
