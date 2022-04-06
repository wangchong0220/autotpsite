# -*- coding:utf-8 -*-
# @Time   :2022/3/20 13:09
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :renderers.py
# 渲染器编写错误会导致页面无内容

from rest_framework.renderers import JSONRenderer


# 自定义渲染器
class MyRenderer(JSONRenderer):
    # 重构render方法
    def render(self, data, accepted_media_type=None, renderer_context=None):
        '''
        :param data: data是请求接受的数据
        :param accepted_media_type: 可以接收的数据类型
        :param renderer_context: 上下文,包含很多数据
        :return:
        '''
        status_code = renderer_context['response'].status_code  # 响应状态码
        if str(status_code).startswith('2'):
            # 处理自定义分页内容
            # 接口定义的data返回是一个列表，所以需要对接口返回数据进行处理
            res = {'msg': 'success', 'retcode': status_code}  # 数据返回模板
            if not isinstance(data, list):  # isinstance(参数1，参数2) 是判断参数1是不是参数2类型
                if 'retlist' not in data:
                    res.update({'retlist':[data]}) # 单条数据的格式,是没有retlist的,所以要给他加上retlist格式
                else:
                    res.update(data)  # 如果data不是一个列表，那就直接更新data
            else:
                res.update({'retlist': data})  # 如果是个列表，就用字典符号套上，并把retlist更新到模板里面
            # 返回父类型方法
            return super().render(res, accepted_media_type, renderer_context)
        else:
            # data是异常数据传过来的最终返回的值
            return super().render(data, accepted_media_type, renderer_context)
