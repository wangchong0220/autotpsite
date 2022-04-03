# -*- coding:utf-8 -*-
# @Time   :2022/3/19 23:17
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :urls.py
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from sqtp import views
# 配合视图集
from rest_framework.routers import DefaultRouter

schema_view = get_schema_view(  # 文档视图
    openapi.Info(
        title='SQTP API DOC',
        default_version='v1',
        description='SQTP接口文档',
        terms_of_service='https://www.songqin.net',
        contact=openapi.Contact(email='haiwen@sqtest.org', url='http://haiwenblog.org'),
        license=openapi.License(name='BSD License')
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)  # permissions.AllowAny允许所有用户
)

router = DefaultRouter()  # 实例化路由器
# 注册路由语法:router.register(r'路由名',视图文件名.路由集合名)
router.register(r'requests', views.RequestViewSet)  # 注册路由 必须要写r
router.register(r'cases', views.CaseViewSet)
router.register(r'steps', views.StepViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'envs', views.EnvironmentViewSet)
router.register(r'plans', views.PlanViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger'),  # 互动模式
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),  # 文档模式
    path('users/', views.user_list),
    path('users/<int:_id>', views.user_detail),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('current_user/', views.current_user)
]
