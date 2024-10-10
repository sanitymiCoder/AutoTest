import pytest
import allure

from testcases import api_excute
from utils.YamlUtil import YamlUtil
from utils.SetFilePath import FILE_PATH

@allure.feature('业务流程测试')
class TestCase:
    
    @allure.story("业务流程")
    @pytest.mark.parametrize('api_info',YamlUtil().read_yaml(FILE_PATH['business']))
    def test_demo(self,api_info):
        allure.dynamic.title(api_info['baseInfo']['api_name'])
        api_excute.api_case_excute(api_info)