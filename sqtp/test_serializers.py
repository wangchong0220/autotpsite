# -*- coding:utf-8 -*-
# @Time   :2022/3/19 22:04
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :test_serializers.py

from django.test import TestCase
from sqtp.models import Step, Request
from .serializers import RequestSerializer
from rest_framework.renderers import JSONRenderer  # 序列化器做序列化的，后端转成前端的json/xml
from rest_framework.parsers import JSONParser  # 反序列化器做反序列化的，前端转成后端的orm对象


class TestRequestSerializers(TestCase):
    req = Request.objects.create(method=1, url='/api/login',
                                 data={'name': 'xiaoming', 'age': 18, 'addr': 'nanjing'})
    # 序列化第一步：将orm数据对象转换成python原生数据类型
    req_serializer = RequestSerializer(req)
    # 序列化后的数据存储于序列化的data属性中,数据类型是python字典数据格式，没有展示None
    print(req_serializer.data)

    # 序列化第二步：将python原生数据类型转换成json
    content = JSONRenderer().render(req_serializer.data)
    # json数据类型前面会有一个b：一个字节，没有展示的是null
    print(content)
    # b'{"step":null,"method":1,"url":"/api/login",
    # "params":null,"headers":null,"cookies":null,
    # "data":{"name":"xiaoming","age":18,"addr":"nanjing"},
    # "json":null}

    # 反序列化第一步：将上面的content传递的数据解析成python数据类型
    # io库是专门用来处理数据流：input，output
    import io
    # 构建一个steam数据流
    steam = io.BytesIO(content)
    # 转换成python的数据类型
    data = JSONParser().parse(steam)
    print(data)

    # 烦序列化第二部：将python的数据类型转换成orm模型实例
    # 反序列化时，代码时不知道前端传来的参数，所以在构建序列化器时需要一个参数接收已转换的python数据
    serializer = RequestSerializer(data=data)
    if serializer.is_valid():  # 校验入参是否合法
        print(serializer.validated_data)  # 如果数据合法，就存到validated_data里面
        serializer.save()

    # 序列化器查看结果集
    serializer = RequestSerializer(Request.objects.all(), many=True)
    print(serializer.data)

    # 序列化器内部代码 repr方法可以查看对象的内部源码
    print(repr(serializer))
