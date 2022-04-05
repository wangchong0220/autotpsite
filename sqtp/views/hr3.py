# -*- coding:utf-8 -*-
# @Time   :2022/3/31 21:08
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :hr3.py
import os

from httprunner import loader, compat
from httprunner.cli import main_run  # 执行用例模块
from rest_framework.parsers import FileUploadParser
from rest_framework.views import APIView

from sqtp.models import Request, Step, Config, Case  # 导入模块
from sqtp.serializers import RequestSerializer, StepSerializer, CaseSerializer, \
    ConfigSerializer
from rest_framework.response import Response  # DRF自带响应格式信息
from rest_framework import status, serializers  # DRF自带响应状态码
# 把通用视图类并成一个视图集合
from rest_framework import viewsets  # 视图集
from django.utils.decorators import method_decorator  # 视图接口美化
from drf_yasg.utils import swagger_auto_schema  # swagger
from rest_framework.decorators import action


# 视图集---增删改查（只针对一组数据进行处理）
# 模型名+ViewSet
@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_summary='列出数据', operation_description='列出请求数据...'))
# web请求视图集
class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


# 配置视图集
class ConfigViewSet(viewsets.ModelViewSet):
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer


# 测试用例视图集
class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    # 用户与数据关联
    # 创建用例和当前登录用户关联
    def perform_create(self, serializer):
        serializer.save(create_by=self.request.user)

    # 更新用例时，和当前用户关联
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    # 运行测试用例接口
    @action(methods=['GET'], detail=True, url_path='run', url_name='run_case')
    # detail=True：调用视图集中自定义方法，需要传入对应的id
    # url路径=run是完整的url路径：/case/<int:case_id>
    def run_case(self, request, pk):
        # 获取序列化器
        case = Case.objects.get(pk=pk)  # 根据id获取当前的用例
        serializer = self.get_serializer(instance=case)  # 获取序列化器数据
        path = serializer.to_json_file()  # 把获取到的序列化器数据进行json转换，生成用例文件
        # API执行法，是HR3自带的执行法
        # main_run运行的是一个列表，所以必须加上[]
        exit_code = main_run([path])
        if exit_code != 0:
            return Response(data={"error": "执行用例失败", "retcode": exit_code},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={'msg': '执行用例成功', 'retcode': status.HTTP_200_OK})


# 测试步骤视图集
class StepViewSet(viewsets.ModelViewSet):
    queryset = Step.objects.all()
    serializer_class = StepSerializer


# 测试用例文件上传
class FileUploadView(APIView):
    parser_classes = [FileUploadParser]  # 指定数据解析

    # 重写put方法
    def put(self, request, filename, format=None):
        # 接收前端传来的文件
        file_list = request.FILES
        if not os.path.exists('upload'):
            os.mkdir('upload')
        for k, v in file_list.items():
            with open(f'upload/{v.name}', 'wb') as f:
                f.write(v.read())  # 写入的是读取的上传文件的内容

        # 去除http文件分隔符，前三行和最后一行
        with open(f'upload/{filename}', ) as f:
            # read() 每次读取整个文件，它通常将读取到底文件内容放到一个字符串变量中，也就是说
            #  read() 生成文件内容是一个字符串类型。
            # readline()每只读取文件的一行，通常也是读取到的一行内容放到一个字符串变量中，返回str类型。
            # readlines()每次按行读取整个文件内容，将读取到的内容放到一个列表中，返回list类型。
            lines = f.readlines()[3:][:-1]  # 过滤前三行和最后一行

        with open(f'upload/{filename}', 'w') as f:
            for line in lines:
                f.write(line)

        # 检查文件内容是否符合hr3格式
        # 调用内部的API（loader_test_file）载入测试文件内容进行解析
        # 载入文件后采用compat.ensure_testcase_v3，接收存进来的内容进行校验
        try:
            content = loader.load_test_file(f'upload/{filename}')
            valid_case = compat.ensure_testcase_v3(content)
        except Exception as e:
            raise serializers.ValidationError(f'错误的hr3用例格式: {repr(e)}')
        # 内容导入到数据库
        valid_case['project_id'] = 5  # 上传用例时的默认关联项目
        serializer = CaseSerializer(data=valid_case)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'retcode': 400, 'msg': 'upload failed',
                             'error': serializer.errors}, status=400)
        return Response({'retcode': 204, 'msg': 'uploading..'})
