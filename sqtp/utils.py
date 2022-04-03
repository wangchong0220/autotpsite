# -*- coding:utf-8 -*-
# @Time   :2022/3/31 15:08
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :demo1.py
# 过滤json文件的数据--接收字典格式数据，过滤非必要数据和非空字段数据。
import os
from pprint import pprint


def filter_data(data):
    # 准备一个HR3模板文件，用来和用例json文件对比
    template = {

        'config': {
            'name': str,
            'base_url': str,
            'variables': dict,
            'parameters': dict,
            'verify': bool,
            'export': list
        },
        'teststeps': [{
            'name': str,
            'variables': list,
            'extract': dict,
            'validate': list,
            'setup_hooks': list,
            'teardown_hooks': list,
            'request': {
                'method': str,
                'url': str,
                'params': list,
                'headers': dict,
                'cookies': dict,
                'data': dict,
                'json': dict
            },
        }]
    }
    return merge_dict(template, data)


def merge_dict(left, right):
    '''
    :param left: 模板文件
    :param right: 测试用例json文件
    :return:
    '''
    '''
    设计思路：
    左边是模板文件，右边是测试用例json文件
    只要遍历右边的文件，并且和左边的文件格式做比对
    相同且不为空就保留,相同且为空就删除右边的空数据
    '''
    # 第一步遍历测试用例的json文件
    for k in right:
        # 判断遍历的k在不在模板里面
        if k in left:
            # 在里面判断左右两边k的属性是不是都为dict
            if isinstance(left[k], dict) and isinstance(right[k], dict):
                merge_dict(left[k], right[k])
            # 在里面判断两边数据k的属性是不是都为list
            elif isinstance(left[k], list) and isinstance(right[k], list):
                for one in right[k]:
                    merge_dict(left[k][0], one)
            # 合并条件：right[k]不为空（也包含空字符串，空列表，空字典）
            elif right[k]:
                left[k] = right[k]  # 如果右侧k对应的数据是对的，就把右侧数据的值付给左侧数据的k
            elif not right[k]:  # 如果右侧数据是空的
                left.pop(k)  # 删除左侧对应的右侧的k为空的数据
    # 当左右两侧数据同步后，左侧的key值不在右侧的话就删除，防止模板多数据
    for k in list(left.keys()):
        if k not in right:
            left.pop(k)

    return left  # 这里的left是已经处理好的数据


def setup_case_dir(case_path):
    empty_dir_files(case_path,'json','py','pyc')


# 每次执行前清空用例目录
def empty_dir_files(path, *suffix):  # suffix是可选参数
    for root, dirs, files in os.walk(path):  # list是浅层遍历，walk是深层遍历
        for fi in files:
            if fi.split('.')[-1] in suffix:
                os.remove(os.path.join(root, fi))
