# -*- coding:utf-8 -*-
# @Time   :2022/3/26 9:44
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :mgr.py

from rest_framework import serializers

from sqtp.models import Project, Environment
from sqtp.serializers import UserSerializer


# 测试项目序列化器
class ProjectSerializer(serializers.ModelSerializer):
    # 格式化输出时间
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    admin_id = serializers.IntegerField(write_only=True)
    admin = UserSerializer(read_only=True)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.get_status_display()

    class Meta:
        model = Project
        fields = ['id', 'admin', 'admin_id', 'name', 'status', 'version',
                  'desc', 'create_time', 'update_time']


# 服务器环境序列化器
class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        fields = '__all__'
