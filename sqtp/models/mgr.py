# -*- coding:utf-8 -*-
# @Time   :2022/3/21 19:57
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :mgr.py
from django.db import models
from .base import CommonInfo
from django.conf import settings  # 导入django自带的settings模块(也就是autotpsite里面的settings)


class Project(CommonInfo):
    PRO_STATUS = (
        (0, '开发中'),
        (1, '维护中'),
        (2, '稳定运行')
    )
    # 管理员
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                              null=True, related_name='project_admin', verbose_name='管理员')
    # 成员
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='project_members',
                                     verbose_name='普通成员')
    # 项目名称
    name = models.CharField(max_length=128, unique=True, null=False, verbose_name='项目名称')
    # 项目状态
    status = models.SmallIntegerField(choices=PRO_STATUS, default=2, verbose_name='项目状态')
    # 项目版本
    version = models.CharField(max_length=32, default='V1.0', verbose_name='项目版本')

    class Meta(CommonInfo.Meta):
        ordering = ["id", '-create_time']
        verbose_name = '项目表'


class Environment(CommonInfo):
    service_type = (
        (0, 'web服务器'),
        (1, '数据库服务器')
    )

    service_os = (
        (0, 'windows'),
        (1, 'linux')
    )
    service_status = (
        (0, 'active'),
        (1, 'disable')
    )
    # 所属项目
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    # IP地址
    ip = models.GenericIPAddressField(default='127.0.0.1', verbose_name='ip地址')
    # 项目端口号
    port = models.SmallIntegerField(default=80, verbose_name='端口')
    # 服务器类型
    category = models.SmallIntegerField(choices=service_type, default=0, verbose_name='服务器类型')
    # 操作系统
    os = models.SmallIntegerField(choices=service_os, default=1, verbose_name='操作系统')
    # 服务器状态
    status = models.SmallIntegerField(choices=service_status, default=0, verbose_name='服务器状态')

    def __str__(self):
        return self.ip + ':' + self.port

    class Meta(CommonInfo.Meta):
        verbose_name = '测试环境表'
