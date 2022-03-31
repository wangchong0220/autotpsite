# # -*- coding:utf-8 -*-
# # @Time   :2022/3/21 21:21
# # @Author :chongwang
# # @Email  :877431474@qq.com
# # @File   :auth.py
#
# from django.contrib.auth.models import AbstractUser
# from django.db import models
#
#
# # 根据django自带的用户权限写一个自己的用户权限
# # 第一步:写一个用户模型
# # 第二步:引入自定义模型:setting.AUTH_USER_MODEL这个模块
# class User(AbstractUser):
#     USER_TYPE = (
#         (0, '开发'),
#         (1, '测试'),
#         (2, '运维'),
#         (3, '项目经理'),
#     )
#     realname = models.CharField('真实姓名', max_length=12)
#     phone = models.CharField('手机号码', max_length=11, unique=True,
#                              null=True, blank=True)
#     user_type = models.SmallIntegerField('用户类型', choices=USER_TYPE, default=1)

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE = (
        (0, '开发'),
        (1, '测试'),
        (2, '运维'),
        (3, '项目经理'),
    )
    # 真实姓名
    realname = models.CharField('真实姓名', max_length=32)
    phone = models.CharField('手机号', max_length=11, unique=True, null=True, blank=True)
    user_type = models.SmallIntegerField('用例类型', choices=USER_TYPE, default=1)
