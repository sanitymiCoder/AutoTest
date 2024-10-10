
import allure
import pytest
from testcases import api_excute,single_api
from utils.SetFilePath import FILE_PATH
from utils.YamlUtil import YamlUtil
from utils.ReplaceYaml import ReplaceYaml



@allure.feature('登录模块')
class TestLogin:
    
    @pytest.mark.run(order=1)
    @pytest.mark.parametrize('base_info,testcase',YamlUtil().read_yaml(FILE_PATH['login']))
    def test_login(self,base_info,testcase):
        allure.dynamic.title(testcase['case_name'])
        #print(api_info['baseinfo']['api_name'])
        #api_info = ReplaceYaml().replace_yaml_variable(api_info)
        result = single_api.api_case_excute(base_info,testcase)
        #print(result)
        
    
    # @pytest.mark.parametrize('caseinfo',YamlUtil().read_yaml(FILE_PATH['testcase']))
    # def test_loginOut(self):
    #    ApiUtil().api_case_excute(caseinfo)
    pass