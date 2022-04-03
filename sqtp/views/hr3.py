# -*- coding:utf-8 -*-
# @Time   :2022/3/31 21:08
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :hr3.py
from httprunner.cli import main_run  # 执行用例模块
from sqtp.models import Request, Step, Config, Case  # 导入模块
from sqtp.serializers import RequestSerializer, StepSerializer, CaseSerializer, \
    ConfigSerializer
from rest_framework.response import Response  # DRF自带响应格式信息
from rest_framework import status  # DRF自带响应状态码
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
