import json
import re
import pytest
import requests
from urllib3 import request

from common.requests_util import RequestsUtil
from common.yaml_util import YamlUtil


class TestCase:

    @pytest.mark.parametrize('caseinfo',YamlUtil().read_testcase_yaml('testcases.yml'))
    def test_login(self,caseinfo):
        method = caseinfo['request']['method']
        url = caseinfo['request']['url']
        data = caseinfo['request']['data']
        print(method, url, data)
        result = RequestsUtil().send_requests(method,url,data)
        print(result)
        result = json.loads(result)
        YamlUtil().write_extract_yaml({"token":result['token']})



    def test_getInfo(self,connet_db):
        url='http://localhost/base/getInfo'

        result = RequestsUtil().send_requests("get",url)
        print(result)


    def test_getRouters(self):
        url='http://localhost/base/getRouters'

        result = RequestsUtil().send_requests("get",url)
        print(result)

    def test_loginOut(self):
        url='http://localhost/base/logout'
        value = YamlUtil().read_extract_yaml("token")
        print(value)
        result = RequestsUtil().send_requests("post",url)



