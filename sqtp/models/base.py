# -*- coding:utf-8 -*-
# @Time   :2022/3/21 19:58
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :base.py
# 公共模型字段
# 模型继承:创建一个公共模型,并在元类设置一个abstract=True的属性
# 其他模型类只需要导入该模型,使用公共模型类名即可CommonInfo
# 模型类面里面的元类如果需要其他模型类的数据继承,需要使用类型.Meta:CommonInfo.Meta
from django.db import models
from django.conf import settings


# 公共模型
class CommonInfo(models.Model):
    # auto_now_add只在新增数据时添加一次时间，后续不会更新
    # 默认可以为空，或者给一个默认值否则会迁移数据库时报错
    # 公共字段部分--创建时间，更新时间，描述,创建者，更新者
    create_time = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    # auto_now_add 第1次创建数据时自动添加当前时间,不用加默认值
    update_time = models.DateTimeField('更新时间', auto_now=True)
    # auto_now 每次更新数据时自动添加当前时间
    desc = models.TextField(null=True, blank=True, verbose_name='描述')
    '''
      在公共通用模型里面使用related_name或者related_query_name参数时
      当其他模型类调用公共模型类时,会把related_name或者related_query_name一起继承过去,但规定这些名称不能重复
      解决方法:在名称前面加入%(class)s:用当前模型子类的小写名替换
              在名称前面加入%(app_label)s:用子类所属app的小写名替换
      '''

    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, verbose_name='创建者',
                                  related_name='%(class)s_create_by')

    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True, verbose_name='更新者',
                                   related_name='%(class)s_updated_by')

    def __str__(self):
        # 判断当前数据对象是否有name属性
        if hasattr(self, 'name'):  # hasattr(self,'name') python中反射的一种用法
            return self.name
        else:
            return self.desc  # 返回描述信息

    class Meta:
        # abstract可以将该模型类变成抽象表，使用迁移数据库时不会在数据库生成这个模型对应的表
        abstract = True  # 当前类为抽象表，字段会被子模型类继承，但是不会创建数据库表 只有abstract这个字段不会被继承
        ordering = ['-create_time']

