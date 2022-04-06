# -*- coding:utf-8 -*-
# @Time   :2022/4/6 21:10
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :pagination.py
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyPageNumberPagination(PageNumberPagination):
    page_size = 5  # 配置默认的页面几个参数，优先级前端传了就按照前端，没传就用这个大小
    page_size_query_param = 'page_size'  # 前端的page_size查询参数
    page_query_param = 'page_index'  # 前端传递的页面参数

    # 覆盖父类的返回数据格式
    def get_paginated_response(self, data):
        resp_data = {
            'retlist': data,  # 分页后的数据
            'total': self.page.paginator.count  # 总数据量
        }
        return Response(resp_data)
