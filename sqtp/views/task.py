# -*- coding:utf-8 -*-
# @Time   :2022/4/3 18:37
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :task.py
import subprocess
import uuid

from httprunner.cli import main_run
from rest_framework.decorators import action

from sqtp.pagination import MyPageNumberPagination
from sqtp.utils import setup_case_dir, collect_log, setup_logs_dir
from sqtp.serializers import PlanSerializer, CaseSerializer
from sqtp.models import Plan, Report
from rest_framework import viewsets, status
from sqtp.serializers.task import ReportSerializer
from rest_framework.response import Response


# 计划视图集
class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    # 同步创建用户
    def perform_create(self, serializer):
        serializer.save(create_by=self.request.user)

    # 更新用例时，和当前用户关联
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    @action(methods=['GET'], detail=True, url_path='run', url_name='run_plan')
    def run_plan(self, request, pk):
        # 通过测试计划id获取对应的测试计划
        plan = Plan.objects.get(pk=pk)
        # 执行的时候更新计划状态并保存
        plan.status = 1
        plan.save()
        setup_case_dir('sqtp/testcase')
        setup_logs_dir('sqtp/logs')
        # 获取测试用例路径
        case_list = []
        for case in plan.cases.all():  # 生成测试用例文件，在收集测试路径
            cs = CaseSerializer(instance=case)
            path = cs.to_json_file()
            case_list.append(path)

        # 采用uuid4创建报告路径
        allure_path = f'report/{uuid.uuid4()}'

        # hr3执行测试用例路径列表文件
        if case_list:
            exit_code = main_run([*case_list, f'--alluredir={allure_path}'])
        else:
            return Response(data={'msg': 'no cases to run', 'retcode': 304}, status=304)
        # 缓存文件转化allure报告(index.html)
        subprocess.Popen(f'allure generate {allure_path} -o dist/{allure_path}', shell=True)

        # 执行后更新计划状态和执行次数
        plan.status = 3
        plan.exec_counts += 1
        plan.save()
        # 获取日志文件
        detail = collect_log('logs')

        # 保存报告数据
        Report.objects.create(plan=plan, path=f'{allure_path}/index.html', trigger=request.user, detail=detail)
        if exit_code != 0:
            return Response(data={"error": "执行计划失败", "retcode": exit_code},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={'msg': '执行计划成功', 'retcode': status.HTTP_200_OK})


# 报告视图集
# 使用ReadOnlyModelViewSet可以让这个视图只读操作,其他接口都会被隐藏
class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    pagination_class = MyPageNumberPagination  # 局部分页器

    # 报告仅供查询
    # def create(self, request, *args, **kwargs):
    #     return Response(data={'msg': 'error', 'retcode': 404, 'error': '创建只针对于测试计划开放'})
    #
    # def update(self, request, *args, **kwargs):
    #     return Response(data={'msg': 'error', 'retcode': 404, 'error': '更新只针对于测试计划开放'})
