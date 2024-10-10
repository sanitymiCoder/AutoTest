import time
import pytest
from datetime import timedelta

from utils.SetFilePath import FILE_PATH
from utils.YamlUtil import YamlUtil
from utils.HandleLogs import logs


# @pytest.fixture(scope="function")
# def connet_db():
#     print("连接数据库")
#     yield
#     print("关闭数据库")


@pytest.fixture(scope="session",autouse=True)
def clear_yaml():
    YamlUtil().clear_yaml(FILE_PATH['extract'])
    
    
@pytest.fixture(scope="function",autouse=True)
def start_end():
    logs.info("==========接口测试开始==========")
    yield
    logs.info("==========接口测试结束==========")





def format_duration(seconds):
    """时间格式化，将秒转成时：分：秒显示"""
    return  str(timedelta(seconds=seconds)).split('.')[0]

def pytest_terminal_summary(terminalreporter,exitstatus,config):
    testcase_total = terminalreporter._numcollected
    passed_num = len(terminalreporter.stats.get('passed',[]))
    failed_num = len(terminalreporter.stats.get('failed',[]))
    error_num = len(terminalreporter.stats.get('error',[]))
    skip_num = len(terminalreporter.stats.get('skiped',[]))
    duration_time = round(time.time()-terminalreporter._sessionstarttime,2)
    format_time = format_duration(duration_time)
    
    #统计通过率，失败率，错误率
    pass_rate =f"{(passed_num/testcase_total)*100:.0f}%" if testcase_total>0 else "N/A"
    fail_rate =f"{(failed_num/testcase_total)*100:.0f}%" if testcase_total>0 else "N/A"
    error_rate =f"{(error_num/testcase_total)*100:.0f}%" if testcase_total>0 else "N/A"
    
    summary = f"""
    自动化测试结束，具体执行结果：
    测试用例总数：{testcase_total}
    用例通过数：{passed_num}
    用例通过率：{pass_rate}
    用例失败数：{failed_num}
    用例失败率：{fail_rate}
    用例错误数：{error_num}
    用例错误率：{error_rate}
    跳过执行数：{skip_num}
    执行总时长：{format_time}({duration_time}s)
    """
    
    print(summary)