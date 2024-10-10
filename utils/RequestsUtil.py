import json
import re

import requests
from utils.ExceptUtil import RequestExceptUtil
from utils.HandleLogs import logs
from utils.YamlUtil import YamlUtil



class RequestsUtil:
    
    def __init__(self) -> None:
        self.session = requests.session()
    
    def text_encode(self,res_text):
        match = re.search(r"\\u[0-9a-fA-F]{4}",res_text)
        if match:
            result = res_text.encode().decode('unicode_escape')
        else:
            result = res_text
        return result

    def send_requests(self,**kwargs):   
        resp = None
        try:
            resp = self.session.request(**kwargs)
            resp.raise_for_status()
            set_cookies = requests.utils.dict_from_cookiejar(resp.cookies)
            if set_cookies:
                YamlUtil().write_yaml(set_cookies)
                #print(f'获取的cookes为:{set_cookies}')
        except requests.Timeout:
            logs.error('网络请求超时')
        except requests.TooManyRedirects:
            logs.error('重定向次数过多')
        except requests.HTTPError as e:
            logs.error(f'HTTP错误：{e.response.status_code}')
        except requests.RequestException:
            logs.error('请求异常')
        except requests.exceptions.ConnectionError as e:
            logs.error(f'接口请求异常，原因：{e}')
        except requests.exceptions.RequestException as e:
             logs.error(f'请求异常，请检查系统或数据是否正常!原因是：{e}')
        return resp
    
    
    def execute_request(self,method,url,headers=None,cookies=None,files=None,api_name=None,case_name=None,**kwargs):
        """_summary_

        Args:
            method (_type_): _description_
            url (_type_): _description_
            data (_type_, optional): _description_. Defaults to None.
            api_name (_type_, optional): _description_. Defaults to None.
            case_name (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        logs.info(f"接口名称：{api_name}")
        logs.info(f"接口地址：{url}")
        logs.info(f"请求方法：{method.upper()}")
        logs.info(f"请求头：{headers}")
        logs.info(f"请求cookies：{cookies}")
        logs.info(f"用例名称：{case_name}")
        
        #获取传参中的请求参数，用于日志打印
        #print(kwargs,type(kwargs))
        if kwargs:
            for params_key,params_value in kwargs.items():
                # print(params_key,params_value)
                # print(type(params_key),type(params_value))
                logs.info(f"参数类型：{params_key}")
                logs.info(f"请求参数：{json.dumps(params_value)}")
        else:
            logs.info("没有请求参数")
               
        response = self.send_requests(method=method,url=url,headers=headers,cookies=cookies,files=files,timeout=10,verify=False,**kwargs)
        print(response.text)
        return response
      