import json
import re
import traceback
import jsonpath
import allure
from utils.AssertUtil import AssertUtil
from utils.ConfigParseUtil import ConfigParseUtil
from utils.RequestsUtil import RequestsUtil
from utils.YamlUtil import YamlUtil
from utils.ReplaceYaml import ReplaceYaml
from utils.ExceptUtil import RequestExceptUtil
from utils.HandleLogs import logs




class SingleApiUtil:
    
    def __init__(self) -> None:
        self.conf = ConfigParseUtil()
        self.send_request = RequestsUtil()
        self.asserts = AssertUtil()
        
        
    def text_encode(self,res_text):
        match = re.search(r"\\u[0-9a-fA-F]{4}",res_text)
        if match:
            result = res_text.encode().decode('unicode_escape')
        else:
            result = res_text
        return result
        
    
    def allure_dict_to_str(self,data):
        """针对allure报告处理字典类型的数据，将其转为字符串并格式化（缩进）
        Args:
            data (_type_): _description_
        Returns:
            _type_: _description_
        """
        if isinstance(data,dict):
            allure_result = json.dumps(data,ensure_ascii=False,indent=4)
        else:
            allure_result = data
        return allure_result
    
    
    def api_case_excute(self,base_info,testcase):
        """执行测试用例
        Args:
            api_info (_type_): 接口信息，读取yaml文件数据
        """
        #print(api_info)
        try:
            #获取并处理接口的基本信息
            host = self.conf.get_env_value('host')
            api_name = base_info['api_name']
            url = host + base_info['url']
            method = base_info['method']
            
            #获取headers，并兼容固定的headers或者调用变量的形式
            headers = base_info.get('headers',None)
            if headers is not None:
                headers = eval(ReplaceYaml().replace_yaml_variable(headers)) if isinstance(headers,str) else headers
           
            #获取cookies，并兼容固定的cookies或者调用变量的形式
            cookies = base_info.get('cookies',None)
            if cookies is not None:
                cookies = eval(ReplaceYaml().replace_yaml_variable(cookies)) if isinstance(cookies,str) else cookies
                
            #获取并处理接口测试用例数据
            case_name = testcase.pop('case_name')
            val_result = ReplaceYaml().replace_yaml_variable(testcase.get('validata',None))
            testcase['validata'] = val_result
            validata = testcase.pop('validata')          
            
            #处理接口返回提取部分
            extract = testcase.pop('extract',None)
            extract_list = testcase.pop('extract_list',None)
            
            #处理参数类型和请求参数
            data_type,data_value = None,None
            for data_type,data_value in testcase.items():
                if data_type in ['json','data','params']:
                    data_value = ReplaceYaml().replace_yaml_variable(data_value)
                    testcase[data_type] = data_value  
                    
            #处理文件上传
            files = testcase.pop('files',None)
            if files:
                for fk,fv in files.items():
                    files = {fk: open(fv,mode='rb')}
            
            response = self.send_request.execute_request(method=method,url=url,headers=headers,cookies=cookies,files=files,api_name=api_name,case_name=case_name,**testcase)
            response.raise_for_status()
            status_code,response_text = response.status_code,self.text_encode(response.text)
            #print(status_code,response_text,response.json())
                
            #定义在allure报告右侧输出的详细信息
            allure_info = {
                '接口名称':api_name,
                '接口地址':url,
                '请求方式':method,
                '请求头':self.allure_dict_to_str(headers if headers else "无需请求头"),
                'Cookies':self.allure_dict_to_str(cookies if cookies else "无需cookies"),
                '测试用例名称':case_name,
                '参数类型':data_type if data_type else "",
                '请求参数':self.allure_dict_to_str(data_value if data_value else "无需请求参数"),
                '接口实际响应信息':self.allure_dict_to_str(response.json())
            }
            for title,content in allure_info.items():
                allure.attach(content,title,attachment_type=allure.attachment_type.JSON)
                
            #处理case中需要提取接口返回的extract数据
            if extract is not None:
                self.extract_data(extract,response_text)
            if extract_list is not None:
                self.extract_data_list(extract_list,response_text)    
                #处理接口断言
            self.asserts.assert_result(validata,response.json(),status_code) 

        except Exception as e:
            logs.error(f'出现未知异常，-{str(traceback.format_exc())}')
            raise RequestExceptUtil(f'出现未知异常,-{e}')
            
            
    def extract_data(self,testcaase_extract,response_text):
        """提取接口返回结果中的单个数据，支持正则表达式和json提取

        Args:
            testcaase_extract (_type_): dict类型，case中的extract的值
            response_text (_type_): str类型，接口返回的结果
        """
        try:
            for key,value in testcaase_extract.items():
               # print(key,value)
                #判断extract里的正则表达式获取组是否在列表中
                if any(pat in value for pat in ['(.*?)','(.+?)',r'(\d+)',r'(\d*)']):
                    ext_list = re.search(value,response_text)
                    extract_data = {key:int(ext_list.group(1)) if r'(\d+)' in value else ext_list.group(1)}
                    #print(f'提取到的extract结果：{extract_data}')
                elif "$" in value:
                    extract_json = jsonpath.jsonpath(json.loads(response_text),value)[0]
                    #print(extract_json)
                    if extract_json:
                        extract_data = {key:extract_json} if extract_json else {key:'未提取到需要的数据，请检查返回信息或提取表达式！'}
                YamlUtil().write_yaml(extract_data)
        except re.error as e:
            logs.error(f'正则表达式错误，请检查yaml文件extract的表达式是否正确！-{e}')
        except json.JSONDecodeError as e:
            logs.error(f'json解析错误，请检查yaml文件extract的表达式是否正确！-{e}')
        except Exception as e:
            logs.error(f'出现未知异常：-{e}')
            
    
    def extract_data_list(self,testcaase_extract_list,response_text):
        """提取接口返回结果中的多个参数，支持正则表达式和json提取
        Args:
            testcaase_extract (_type_): dict类型，case中的extract的值
            response_text (_type_): str类型，接口返回的结果
        """
        try:
            for key,value in testcaase_extract_list.items():
                #print(key,value)
                #判断extract里的正则表达式获取组是否在列表中
                if any(pat in value for pat in ['(.*?)','(.+?)',r'(\d+)',r'(\d*)']):
                    ext_list = re.findall(value,response_text,re.S)
                    #print(ext_list)
                    if ext_list:
                        extract_data = {key:ext_list}
                elif "$" in value:
                    extract_json = jsonpath.jsonpath(json.loads(response_text),value)
                    #print(extract_json)
                    if extract_json:
                        extract_data = {key:extract_json} if extract_json else {key:'未提取到需要的数据，请检查返回信息或提取表达式！'}
                        #print(extract_data)
                YamlUtil().write_yaml(extract_data)
        except re.error as e:
            logs.error(f'正则表达式错误，请检查yaml文件extract的表达式是否正确！-{e}')
        except json.JSONDecodeError as e:
            logs.error(f'json解析错误，请检查yaml文件extract的表达式是否正确！-{e}')
        except Exception as e:
            logs.error(f'出现未知异常：-{e}')