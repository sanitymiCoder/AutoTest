
import allure
import pytest
from testcases import api_excute,single_api
from utils.SetFilePath import FILE_PATH
from utils.YamlUtil import YamlUtil


@allure.feature("获取列表信息")
class TestGetList:
    

    @pytest.mark.parametrize('baseInfo,testcase',YamlUtil().read_yaml(FILE_PATH['getRouters']))
    def test_getRouters(self,baseInfo,testcase):
        print(f'获取的参数======{baseInfo}')
        print(f'获取的参数======{testcase}')
        allure.dynamic.title(testcase['case_name'])
        single_api.api_case_excute(baseInfo,testcase)


    @pytest.mark.parametrize('baseInfo,testcase',YamlUtil().read_yaml(FILE_PATH['getInfo']))
    def test_getInfo(self,baseInfo,testcase):
        allure.dynamic.title(testcase['case_name'])
        #api_info = yaml_util.replace_yaml_variable(api_info)
        result = single_api.api_case_excute(baseInfo,testcase)
        #print(result)
        

    @pytest.mark.parametrize('baseInfo,testcase',YamlUtil().read_yaml(FILE_PATH['configList']))
    def test_getConfigList(self,baseInfo,testcase):
        allure.dynamic.title(testcase['case_name'])
        #api_info = yaml_util.replace_yaml_variable(api_info)
        result = single_api.api_case_excute(baseInfo,testcase)
        #print(result)

     
    @pytest.mark.parametrize('baseInfo,testcase',YamlUtil().read_yaml(FILE_PATH['dictList']))
    def test_getDictList(self,baseInfo,testcase):
        allure.dynamic.title(testcase['case_name'])
        #api_info = yaml_util.replace_yaml_variable(api_info)
        result = single_api.api_case_excute(baseInfo,testcase)
        #print(result)
      

    @pytest.mark.parametrize('baseInfo,testcase',YamlUtil().read_yaml(FILE_PATH['userList']))
    def test_getUserList(self,baseInfo,testcase):
        allure.dynamic.title(testcase['case_name'])
        #api_info = yaml_util.replace_yaml_variable(api_info)
        result = single_api.api_case_excute(baseInfo,testcase)
        
    @pytest.mark.parametrize('baseInfo,testcase',YamlUtil().read_yaml(FILE_PATH['deptList']))
    def test_getDeptList(self,baseInfo,testcase):
        allure.dynamic.title(testcase['case_name'])
        #api_info = yaml_util.replace_yaml_variable(api_info)
        result = single_api.api_case_excute(baseInfo,testcase)