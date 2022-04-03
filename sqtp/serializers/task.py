# -*- coding:utf-8 -*-
# @Time   :2022/4/3 18:35
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :task.py
from rest_framework import serializers
from sqtp.models import Plan


# 测试计划序列化器
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'
