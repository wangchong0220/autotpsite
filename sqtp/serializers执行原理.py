# -*- coding:utf-8 -*-
# @Time   :2022/3/19 21:36
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :serializers.py
# 序列化器：构造序列化和反序列化
# 序列化是把后端orm模型传递出来的数据对象转换成json/xml格式的前端数据
# 反序列化是把前端json/xml数据转换成orm模型数据对象

from rest_framework import serializers  # 导入序列化器
from .models import Step, Request


# 序列化器是针对数据模型，一个序列化器对应一个模型，不可以对应多个模型
# 命名规范：模型名+Serializer
class RequestSerializer(serializers.ModelSerializer):  # 继承序列化器
    method_choice = (  # 二维元组(())
        (0, 'GET'),  # 参数1是实际存储在库里面的值，参数2是对外展示的值
        (1, 'POST'),
        (2, 'PUT'),
        (3, 'DELETE')
    )
    # queryset是一个查询集，接收查询到的step的所有数据,allow_null=True是可以为空
    step = serializers.RelatedField(queryset=Step.objects.all(),
                                    allow_null=True)
    method = serializers.ChoiceField(choices=method_choice, default=0)  # choices指定默认取值范围，default默认取值
    url = serializers.CharField(allow_null=True)
    params = serializers.JSONField(allow_null=True)
    headers = serializers.JSONField(allow_null=True)
    cookies = serializers.JSONField(allow_null=True)
    data = serializers.JSONField(allow_null=True)
    json = serializers.JSONField(allow_null=True)

    # 重写创建和修改方法
    # 在模型中给数据确定了类型（RelatedField，JSONField等）
    # 框架想要通过序列化器调用数据，必须通过校验化器，校验化器校验之后
    # 会把数据存储在validated里面，框架自动调用的时候也会把数据存到这里面
    def create(self, validated_data):
        '''
        :param validated_data: 经过校验器，校验之后通过的数据，validated_data是一个字典类型的值
        '''
        # 对通过校验的数据进行解包，相当于根据每个字典的key找到每一行的值：name：xxx，url：xxx
        return Request.objects.create(**validated_data)

    # 根据提供校验之后的数据返回一个新的对象/实例
    def update(self, instance, validated_data):
        '''
        :param instance: 被修改的数据对象/实例
        :param validated_data: 经过校验之后的数据
        '''
        # validated_data调用字典里得值使用get方法
        # get(参数1是key,参数2是默认值)，get方法会通过key找到对应的value，如果value没有值则为空
        # 但根据业务，有新的数据才把之前的数据给覆盖，没有新的数据应该返回之前的数据，所以需要在后面加入原来的值
        instance.step = validated_data.get['step', instance.step]
        instance.method = validated_data.get['method', instance.method]
        instance.url = validated_data.get['url', instance.url]
        instance.params = validated_data.get['params', instance.params]
        instance.headers = validated_data.get['headers', instance.headers]
        instance.cookies = validated_data.get['cookies', instance.cookies]
        instance.data = validated_data.get['data', instance.data]
        instance.json = validated_data.get['json', instance.json]

