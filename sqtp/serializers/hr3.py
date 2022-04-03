# -*- coding:utf-8 -*-
# @Time   :2022/3/26 9:43
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :hr3.py
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from sqtp.models import Request, Step, Config, Case, Project
from sqtp.serializers import ProjectSerializer, UserSerializer
from sqtp.utils import filter_data
from rest_framework.exceptions import ValidationError


# web请求序列化器
class RequestSerializer(serializers.ModelSerializer):
    method = serializers.SerializerMethodField()  # 指定该字段被底下的get_method获取，这是框架设计的固定写法
    step_id = serializers.IntegerField(write_only=True, required=False)  # 配合Step序列化器的字段是用

    # request的参数只是配合step写入，但是不一定必填

    # SerializerMethodField()这个对象会字段调用get_method方法，并把获取的数据注入到obj上
    # 获取二维数组展示内容
    def get_method(self, obj):
        return obj.get_method_display()

    class Meta:
        model = Request  # 指定该序列器对应的模型
        # fields = ['step','method',.....] 指定部分序列化字段，些什么字段名就序列化哪些字段
        fields = ['step_id', 'method', 'url', 'params', 'headers', 'json', 'data']  # 指定序列化的字段，__all__是所有的字段

    # 批量自定义校验器
    def validate(self, attrs):
        template = {
            'params': dict,
            'headers': dict,
            'cookies': dict
        }
        for param_name, type_name in template.items():
            if param_name in attrs and not isinstance(attrs[param_name], type_name):
                raise ValidationError(f'请输入正确的{param_name}格式：{type_name}')
        return attrs


# web配置序列化器
class ConfigSerializer(serializers.ModelSerializer):
    # 在前端页面创建case时，需要传入project_id
    # 但因为project是在case序列化器里面创建的，所以这里只能使用，不能创建
    project = ProjectSerializer(required=False, read_only=True)

    class Meta:
        model = Config
        fields = ['project', 'name', 'base_url', 'variables', 'parameters', 'export', 'verify']

    def validate(self, attrs):
        template = {
            'variables': dict,
            'parameters': dict,
            'export': list,
            'base_url': str
        }
        for param_name, type_name in template.items():
            if param_name in attrs and not isinstance(attrs[param_name], type_name):
                # 数据类型校验
                raise ValidationError(f'请传递正确的{param_name}格式: {type_name}')
            # 再加入base_url格式检测--是否以http://或https://开头
            if not 'base_url'.startswith('http://'):
                raise ValidationError('请输入正确的url，以http://开头')
        return attrs


# 测试步骤序列化器
class StepSerializer(serializers.ModelSerializer):
    request = RequestSerializer()
    belong_case_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        # 先筛选出传入的request参数
        req_kws = validated_data.pop('request')
        # 构造步骤
        step_obj = Step.objects.create(**validated_data)
        # 构造请求前先将step_obj传入参数里面
        req_kws['step_id'] = step_obj.id
        req_serializer = RequestSerializer(data=req_kws)
        if req_serializer.is_valid():
            req_obj = req_serializer.save()
        # else:
        #     return ValidationError(req_serializer.errors)

        return step_obj

    class Meta:
        model = Step
        fields = ['name', 'variables', 'request', 'extract', 'validate',
                  'setup_hooks', 'teardown_hooks', 'belong_case_id', 'sorted_no']

    def validate(self, attrs):
        template = {
            'variables': dict,
            'request': dict,
            'extract': dict,
            'validate': list,
            'setup_hooks': list,
            'teardown_hooks': list,
        }
        for param_name, type_name in template.items():
            if param_name in attrs and not isinstance(attrs[param_name], type_name):
                raise ValidationError[f'请输入正确的{param_name}的格式：{type_name}']
        return attrs


# 测试用例序列化器
class CaseSerializer(serializers.ModelSerializer):
    config = ConfigSerializer()  # config字段就对应其序列化器返回的内容
    # 创建用例的时候不创建步骤，只有在用例编辑时候才会加入步骤，所以必须使用required=False不必填或者read_only只读，就不会校验入参了
    # required=False表示非必填，且可以获取到对应传入的参数，read_only只能被读取，不能获取参数
    teststeps = StepSerializer(required=False, many=True)  # many=True是数据以列表形式展示
    project_id = serializers.CharField(write_only=True)  # 序列化器定义的字段必须在fields出现
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    create_by = UserSerializer(read_only=True, required=False)
    updated_by = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Case
        fields = ['config', 'teststeps', 'project_id', 'desc', 'id', 'file_path',
                  'create_time', 'update_time', 'create_by', 'updated_by']  # 模型里面定义的字段可以直接写
        # 序列化器定义的字段必须在这里写出来

    # 新增测试用例
    def create(self, validated_data):
        '''
        :param validated_data: 校验之后的数据
        :return:
        '''
        config_kws = validated_data.pop('config')  # 弹出校验后的数据里面的config数据
        project = Project.objects.get(pk=validated_data.pop('project_id'))  # 取出校验后数据里面的project_id
        config = Config.objects.create(project=project, **config_kws)  # 将config关联到用例里面
        file_path = f'{project.name}_{config.name}.json'  # 创建case后转成json数据,使用.json即可完成转换
        # 创建用例
        case = Case.objects.create(config=config, file_path=file_path, **validated_data)
        return case

    # 修改测试用例
    def update(self, instance, validated_data):
        '''
        instance 当前被修改的数据对象
        validated_data 校验后的入参--字典形式
        '''
        config_kws = validated_data.pop('config')  # config入参
        project = Project.objects.get(pk=validated_data.pop('project_id'))
        # 把project数据传递到config入参中
        config_kws['project'] = project.id
        conf_serializer = ConfigSerializer(instance=instance.config, data=config_kws)
        # 通过序列化器更新数据
        if conf_serializer.is_valid():
            conf_serializer.save()  # 调用save方法之前必须调用检查参数动作
        else:
            raise ValidationError(conf_serializer.errors)  # 发生错误后，信息保存在序列化器的error字段中

        # teststeps更新
        # 更新之前先删除当前用例已经关联的step
        step_qs = instance.teststeps.all()
        for step in step_qs:
            step.delete()
        # 然后在重新关联

        teststeps = validated_data.pop('teststeps')
        for step in teststeps:
            # 取出步骤关联的用例ID
            step['belong_case'] = self.instance.id
            ss = StepSerializer(data=step)
            if ss.is_valid():
                ss.save()
            else:
                raise ValidationError(ss.errors)
        ...
        # 修改case
        # 利用python反射自动赋值
        for k, v in validated_data.items():
            # 注意validated_data不要包含instance数据对象没有的字段参数
            setattr(instance, k, v)
        instance.save()  # 修改后保存到数据库
        return instance

        # 生成hr3格式的json文件

    def to_json_file(self, path=None):
        if path is None:
            path = self.instance.file_path  # 如果没传就采用用例自己的文件路径
        if not path.endswith('json'):
            path = path + 'json'
        # 生成的用例文件存放在项目目录的testcase下 f'XXX'格式化输出
        path = f'sqtp/testcase/{path}'

        # 过滤输出data
        valid_data = filter_data(self.data)
        # 最后把文件转成json
        # 要把data对象转换成字节
        # 获取文件内容--bytes
        content = JSONRenderer().render(self.data, accepted_media_type='application/json;indent=4')
        # 再把字符串转写入json文件
        with open(path, 'wb') as f:
            f.write(content)
        return path
