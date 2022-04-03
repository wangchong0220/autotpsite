# -*- coding:utf-8 -*-
# @Time   :2022/3/31 21:07
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :__init__.py.py
from .mgr import EnvironmentViewSet, ProjectViewSet
from .hr3 import ConfigViewSet, CaseViewSet, RequestViewSet, StepViewSet
from .auth import current_user, login, logout, register, user_list, user_detail
from .task import PlanViewSet,ReportViewSet