# -*- coding:utf-8 -*-
# @Time   :2022/3/31 21:08
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :mgr.py

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from sqtp.models import Project, Environment  # 导入模块
from sqtp.permissions import IsOwnerOrReadOnly  # 导入自定义的权限类
from sqtp.serializers import ProjectSerializer, EnvironmentSerializer

# 把通用视图类并成一个视图集合
from rest_framework import viewsets  # 视图集


# 测试项目视图集
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # 项目只允许当前的管理员编辑：局部认证
    authentication_classes = (BasicAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


# 环境视图集
class EnvironmentViewSet(viewsets.ModelViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer
    permission_classes = (())  # 将局部不需要设置全面的模块传入空的元组就可以禁用全局权限
