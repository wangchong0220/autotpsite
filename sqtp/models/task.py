# -*- coding:utf-8 -*-
# @Time   :2022/4/3 18:23
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :task.py
# 测试计划+测试报告模块

from django.conf import settings
from django.db import models
from .base import CommonInfo
from .hr3 import Case
from .mgr import Environment


# 计划模型
class Plan(CommonInfo):
    status_choice = (
        (0, "未运行"),
        (1, "执行中"),
        (2, "执行中断"),
        (3, "已执行")
    )
    # blank允许为空
    # 绑定用例
    cases = models.ManyToManyField(Case, verbose_name='测试用例', help_text='测试用例', blank=True)
    # 执行者
    executor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True,
                                 verbose_name='执行人员')
    # 测试环境
    environment = models.ForeignKey(Environment, on_delete=models.SET_NULL, null=True,
                                    verbose_name='测试环境')
    # 状态
    status = models.SmallIntegerField(choices=status_choice, default=0, verbose_name='执行状态')
    # 执行次数
    exec_counts = models.PositiveSmallIntegerField(default=0, verbose_name='执行次数')
    # 计划名称
    name = models.CharField('测试计划', max_length=32)

    class Meta(CommonInfo.Meta):
        pass


class Report(CommonInfo):
    # 关联计划
    plan = models.ForeignKey(Plan, on_delete=models.DO_NOTHING, verbose_name='测试计划')
    # 路径
    path = models.CharField('报告路径', max_length=500)
    # 保存报告详情
    detail = models.TextField('报告详情')
    # 执行人
    trigger = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.DO_NOTHING, null=True)

