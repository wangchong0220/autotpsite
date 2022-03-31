# -*- coding:utf-8 -*-
# @Time   :2022/3/31 21:07
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :auth.py
from sqtp.serializers import UserSerializer, RegisterSerializer, LoginSerializer  # 导入自定义序列化器
from rest_framework.response import Response  # DRF自带响应格式信息
from rest_framework.decorators import api_view, authentication_classes, permission_classes  # DRF自带请求方法,全局认证信息
from rest_framework import status  # DRF自带响应状态码
from django.contrib import auth  # 导入django自带的权限信息
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from sqtp.models.auth import User  # 权限导入User


# 用户列表视图
@api_view(['GET'])
@authentication_classes((BasicAuthentication, SessionAuthentication))  # 方式三 全局认证
@permission_classes((IsAuthenticated,))  # 方式三 全局权限
def user_list(request):
    query_set = User.objects.all()
    serializer = UserSerializer(query_set, many=True)
    return Response(serializer.data)


# 用户详情视图
@api_view(['GET'])
def user_detail(request, _id):
    try:
        user = User.objects.get(pk=_id)
    except User.DoesNotExist:  # 自带的异常模型
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(instance=user)
    return Response(serializer.data)


# 注册用户
@api_view(['POST'])
@permission_classes(())
def register(request):
    # 获取注册信息的序列化器
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():  # 根据序列化器检查数据是否合法
        user = serializer.register()  # 创建用户数据
        auth.login(request, user)  # 使用django自带的模块去自动生成session,参数一：请求，参数二：用户对象
        return Response(data={'msg': 'register success', 'is_admin': user.is_superuser,
                              'retcode': status.HTTP_201_CREATED},  # 响应体：后端返回给前端的数据
                        # 响应头
                        status=status.HTTP_201_CREATED)
    return Response(data={'msg': 'error', 'retcode': status.HTTP_400_BAD_REQUEST,
                          'error': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)


# 登录视图
@api_view(['POST'])
@permission_classes(())
def login(request):
    # 获取登录信息--序列化器
    serializer = LoginSerializer(data=request.data)
    user = serializer.validate(request.data)  # 在这里使用校验器校验数据
    if user:
        auth.login(request, user)
        # 响应的data数据里面可以放：提示信息，跳转页面，状态码
        return Response(data={'msg': 'login success', 'to': 'index.html'},
                        status=status.HTTP_302_FOUND)
    return Response(data={'msg': 'error', 'retcode': status.HTTP_400_BAD_REQUEST,
                          'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# 登出视图
@api_view(['GET'])
def logout(request):
    # 通过request.user就可以获取用户登录对象了
    # is_authenticated是用来判断用户是否登录
    if request.user.is_authenticated:
        auth.logout(request)  #
    return Response(data={'msg': 'logout success', 'to': 'login.html'},
                    status=status.HTTP_302_FOUND)


# 当前用户信息
@api_view(['GET'])
@permission_classes(())
def current_user(request):
    # 判断下当前用户是否处于登陆状态
    if request.user.is_authenticated:
        # 使用序列化器校验请求之中的user数据
        # 如果user数据正确就返回当前登录用户的登录信息
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data)
    return Response(data={'msg': '没有登录', 'to': 'login.html', 'retcode': status.HTTP_403_FORBIDDEN},
                    status=status.HTTP_403_FORBIDDEN)
