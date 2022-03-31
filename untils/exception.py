# -*- coding:utf-8 -*-
# @Time   :2022/3/20 20:16
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :exception.py
from rest_framework import exceptions
from rest_framework.views import exception_handler, Response


def my_exception_handler(exc, content):
    '''
    :param exc: 异常信息
    :param content:  上下文管理器
    :return:
    '''
    # 获取标准错误响应
    # exception_handler必须传入两个参数：exc,content，可以由my_exception_handler传给exception_handler
    # 通过内置的exception_handler拿到response的异常信息exc
    # 然后异常最新最终存储的是渲染器里的data里面
    error_response = exception_handler(exc, content)
    if error_response:  # 第一步：判断error_response是否属于为空
        if isinstance(exc, exceptions.APIException):  # 第二步：判断异常是否属于APIException
            error_msg = exc.detail
        else:
            # 如果不属于APIException就属于另外两种异常：django原生Http404或者permissionDenied(权限)
            # 这两种异常是没有detail数据的
            # 是这两种就直接返回exc异常信息即可
            error_msg = exc
        # 异常信息的data的模板
        error_response.data = {
            'msg': 'error',
            'retcode': error_response.status_code,
            'error': str(error_msg)
        }
    return error_response
