from django.test import TestCase

# Create your tests here.

from sqtp.models import Request, Case, Config, Step


class TestRelateQuery(TestCase):
    # 单元测试-创建测试用例
    def test_request(self):
        req = Request.objects.filter(url__contains='login')
        print(req)
