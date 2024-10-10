import pytest
import allure

from testcases import api_excute
from utils.ReplaceYaml import ReplaceYaml
from utils.SetFilePath import FILE_PATH


# @allure.feature('文件上传模块')
# class TestFileLoad:
    
#     @pytest.mark.parametrize('api_info',YamlUtil().read_yaml(FILE_PATH['fileUpload']))
#     def test_fileUpload(self,api_info):
#         allure.dynamic.title(api_info['baseInfo']['api_name'])
#         #api_info = ReplaceYaml().replace_yaml_variable(api_info)
#         result = api_excute.api_case_excute(api_info)
#         print(result)
