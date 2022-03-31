# -*- coding:utf-8 -*-
# @Time   :2022/3/26 9:58
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :permission.py
# 权限页面
from rest_framework import permissions


# 自定义权限类
class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
    自定义权限模块，只允许管理员编辑
    重写has_object_permission方法
    '''

    def has_object_permission(self, request, view, obj):
        # 如果访问的方法在权限里面safe_methods包括的
        # 就返回真
        if request.method in permissions.SAFE_METHODS:
            return True
        # 判断当前对象是否属于该项目
        return obj.admin == request.user
