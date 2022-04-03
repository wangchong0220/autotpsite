# -*- coding:utf-8 -*-
# @Time   :2022/4/3 18:37
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :task.py
from sqtp.serializers import PlanSerializer
from sqtp.models import Plan
from rest_framework import viewsets


# 视图集
class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
