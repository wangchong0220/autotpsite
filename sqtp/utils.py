# -*- coding:utf-8 -*-
# @Time   :2022/3/31 15:08
# @Author :chongwang
# @Email  :877431474@qq.com
# @File   :demo1.py
# 过滤json文件的数据--接收字典格式数据，过滤非必要数据和非空字段数据。
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


if __name__ == '__main__':
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
    data = {
    "config": {
        "project": {
            "id": 5,
            "admin": {
                "date_joined": "2022-03-27T07:06:59.427618Z",
                "email": "877431474@qq.com",
                "id": 3,
                "is_active": True,
                "is_superuser": True,
                "phone": "13514236578",
                "realname": "王崇",
                "username": "wangchong",
                "user_type": 1
            },
            "name": "测试三期",
            "status": "开发中",
            "version": "1",
            "desc": "ck_三期",
            "create_time": "2022-03-27 07:17:40",
            "update_time": "2022-03-27 07:17:40"
        },
        "name": "case0022",
        "base_url": "http://localhost",
        "variables": None,
        "parameters": None,
        "export": None,
        "verify": False
    },
    "teststeps": [
        {
            "name": "step_001",
            "variables": {},
            "request": {
                "method": "GET",
                "url": "/demo/path",
                "params": None,
                "headers": None,
                "json": None,
                "data": None
            },
            "extract": {},
            "validate": {},
            "setup_hooks": [],
            "teardown_hooks": [],
            "belong_case_id": 8,
            "sorted_no": 1
        },
        {
            "name": "step_002",
            "variables": {},
            "request": {
                "method": "GET",
                "url": "/demo/path",
                "params": None,
                "headers": None,
                "json": None,
                "data": None
            },
            "extract": {},
            "validate": {},
            "setup_hooks": [],
            "teardown_hooks": [],
            "belong_case_id": 8,
            "sorted_no": 2
        }
    ],
    "desc": "测试用例2",
    "id": 8,
    "file_path": "测试三期_case0022.json",
    "create_time": "2022-03-27 11:10:03",
    "update_time": "2022-03-31 08:29:44",
    "create_by": None,
    "updated_by": {
        "date_joined": "2022-03-27T07:06:59.427618Z",
        "email": "877431474@qq.com",
        "id": 3,
        "is_active": True,
        "is_superuser": True,
        "phone": "13514236578",
        "realname": "王崇",
        "username": "wangchong",
        "user_type": 1
    }
}
    mg = merge_dict(template, data)
    pprint(mg)
