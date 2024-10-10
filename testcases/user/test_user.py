
import allure
import pytest
from testcases import api_excute,single_api
from utils.SetFilePath import FILE_PATH
from utils.YamlUtil import YamlUtil
from utils.HandleLogs import logs
from utils.ReplaceYaml import ReplaceYaml


@allure.feature("用户信息模块")
class TestUser:
    
    @pytest.mark.parametrize('baseInfo,testcase',YamlUtil().read_yaml(FILE_PATH['userEdit']))
    def test_userEdit(self,baseInfo,testcase):
        allure.dynamic.title(testcase['case_name'])
        #api_info = ReplaceYaml().replace_yaml_variable(api_info)
        result = single_api.api_case_excute(baseInfo,testcase)
        #print(result)