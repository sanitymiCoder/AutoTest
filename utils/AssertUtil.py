import operator
from typing import Any, Callable
from utils.DatabaseUtil import ConnectMysql
from utils.ExceptUtil import AssertExceptUtil
from utils.HandleLogs import logs
import jsonpath
import allure



class AssertUtil:
    """接口断言封装
    1）状态码断言
    2）包含模式断言
    3）相等断言
    4）不相等断言
    5）数据库断言
    """
    
    def status_code_assert(self,expected_result,status_code):
        """接口响应状态码断言
        Args:
            expected_result (_type_): yaml文件中的预期状态码
            status_code (_type_): 接口实际返回的状态码
        """
        #断言状态标识：0:表示成功，其他表示失败
        failure_count = 0
        if not isinstance(expected_result,int):
            expected_result = int(expected_result)
        if expected_result == status_code:
            logs.info(f'状态码断言成功：接口实际返回状态码【{status_code}】 == 预期结果【{expected_result}】')
            allure.attach(f"预期结果:{str(expected_result)}\n实际结果:{str(status_code)}","状态码断言结果：成功",attachment_type=allure.attachment_type.JSON)
        else:
            logs.info(f'状态码断言失败：接口实际返回状态码【{status_code}】 != 预期结果【{expected_result}】')
            allure.attach(f"预期结果:{str(expected_result)}\n实际结果:{str(status_code)}","状态码断言结果：失败",attachment_type=allure.attachment_type.JSON)
            failure_count += 1
        return failure_count
    
    
    def contain_assert(self,expected_result,response):
        """字符串包含模式，断言预期结果字符串是否包含在实际响应信息中
        Args:
            expected_result (_type_): dict,yaml文件中预期数据
            response (_type_): dict，接口实际响应信息
        Returns:
            _type_: _description_
        """
        #断言状态标识：0:表示成功，其他表示失败
        failure_count = 0
        for assert_key,assert_value in expected_result.items():
            #print(assert_key,assert_value)
            result_list = jsonpath.jsonpath(response,f'$..{assert_key}')
            #print(result_list)
            if result_list and isinstance(result_list[0],str):
                result_str = ''.join(result_list)
                
                success_message = f'包含断言成功，预期结果【{assert_value}】存在于实际返回结果【{result_str}】中'
                failed_message = f'包含断言失败，预期结果【{assert_value}】未在实际返回结果【{result_str}】中找到'
                if assert_value in result_str:
                    logs.info(success_message)
                    allure.attach(f"预期结果:{assert_value}\n实际结果:{result_str}","包含断言结果：成功",attachment_type=allure.attachment_type.JSON)
                else:
                    failure_count += 1
                    logs.info(failed_message)
                    allure.attach(f"预期结果:{assert_value}\n实际结果:{result_str}","包含断言结果：失败",attachment_type=allure.attachment_type.JSON)
        return failure_count
    
    
    def equal_assert(self,expected_result,response):
        """相等断言，断言预期结果字符串是否等于实际响应信息中的值
        Args:
            expected_result (_type_): （dict）,yaml文件中预期数据
            response (_type_): （dict），接口实际响应信息
        Returns:
            _type_: _description_
        """
        #断言状态标识：0:表示成功，其他表示失败
        failure_count = 0
        if isinstance(response,dict) and isinstance(expected_result,dict):
            #找出实际结果和预期结果共同的key值
            common_keys = list(expected_result.keys() & response.keys())
            if common_keys:
                common_keys = common_keys[0]
                #根据相同的key值去实际结果中获取value，并返回一个实际结果的字典
                actual_result = {common_keys:response[common_keys]}
                #print(actual_result)
                eq_result = operator.eq(actual_result,expected_result)
                if eq_result:
                    logs.info(f'相等断言成功，实际响应结果【{actual_result}】== 预期结果【{expected_result}】')
                    allure.attach(f"预期结果:{expected_result}\n实际结果:{actual_result}","相等断言结果：成功",attachment_type=allure.attachment_type.JSON)
                else:
                    failure_count += 1
                    logs.info(f'相等断言失败，实际响应结果【{actual_result}】!= 预期结果【{expected_result}】')
                    allure.attach(f"预期结果:{expected_result}\n实际结果:{actual_result}","相等断言结果：失败",attachment_type=allure.attachment_type.JSON)
            else:
                failure_count += 1
                logs.debug('相等断言失败，请检查yaml文件和接口返回的key值是否一致')
        return failure_count
    
    
    def not_equal_assert(self,expected_result,response):
        """不相等断言，断言预期结果字符串不等于实际响应信息中的值
        Args:
            expected_result (_type_): （dict）,yaml文件中预期数据
            response (_type_): （dict），接口实际响应信息
        Returns:
            _type_: _description_
        """
        #断言状态标识：0:表示成功，其他表示失败
        failure_count = 0
        if isinstance(response,dict) and isinstance(expected_result,dict):
            #找出实际结果和预期结果共同的key值
            common_keys = list(expected_result.keys() & response.keys())
            if common_keys:
                common_keys = common_keys[0]
                #根据相同的key值去实际结果中获取value，并返回一个实际结果的字典
                actual_result = {common_keys:response[common_keys]}
                #print(actual_result)
                eq_result = operator.ne(actual_result,expected_result)
                if eq_result:
                    logs.info(f'不相等断言成功，实际响应结果【{actual_result}】!= 预期结果【{expected_result}】')
                    allure.attach(f"预期结果:{expected_result}\n实际结果:{actual_result}","不相等断言结果：成功",attachment_type=allure.attachment_type.JSON)
                else:
                    failure_count += 1
                    logs.info(f'不相等断言失败，实际响应结果【{actual_result}】== 预期结果【{expected_result}】')
                    allure.attach(f"预期结果:{expected_result}\n实际结果:{actual_result}","不相等断言结果：失败",attachment_type=allure.attachment_type.JSON)
            else:
                failure_count += 1
                logs.debug('不相等断言失败，请检查yaml文件和接口返回的key值是否一致')
        return failure_count
    
    
    def database_assert(self,expected_result,status_code=None):
        """数据库断言
        Args:
            expected_result (_type_): yaml文件db模式中的语句
            response (_type_): _description_
        """
        #断言状态标识：0:表示成功，其他表示失败
        failure_count = 0
        conn = ConnectMysql()
        db_value = conn.query(expected_result)
        if db_value is not None:
            logs.info('数据库断言成功')
            #allure.attach(f"{str(db_value)}","数据库断言成功",attachment_type=allure.attachment_type.JSON)
        else:
            failure_count += 1
            logs.info('数据库断言失败，没有找到该数据')
    
    
    def assert_result(self,expected_result,response,status_code):
        """断言主函数，通过all_flag标记，all_flag==0表示测试成功，否则失败
        Args:
            expected_result (_type_): list,yaml文件中validata下的预期结果
            response (_type_): 接口实际响应结果
            status_code (_type_): 接口返回状态码
        """
        all_flag = 0
        assert_methods={
            'code':self.status_code_assert,
            'contain':self.contain_assert,
            'eq':self.equal_assert,
            'ne':self.not_equal_assert,
            'db':self.database_assert
        }
        try:
            #print(expected_result)
            for expected in expected_result:
                for assert_mode,assert_value in expected.items():
                    #表示assert_method是一个接受两个参数，参数类型为任意类型，并返回可调用的对象
                    assert_method:Callable[[Any,Any],int] = assert_methods.get(assert_mode)
                    if assert_method:
                        #调用对应的断言方法，传递不同的参数
                        if assert_mode in ['code','db']:
                            flag = assert_method(assert_value,status_code)
                        else:
                            flag = assert_method(assert_value,response)
                        all_flag += flag
                    else:
                        #print(f'暂时不支持{assert_method}断言模式')
                        raise AssertExceptUtil(f'暂时不支持{assert_method}断言模式')            
        except Exception as e:
            #print(f'未知异常，{e}')
            raise e
        
        assert all_flag == 0,'测试失败'
        logs.info('测试成功')