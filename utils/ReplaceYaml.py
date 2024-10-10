
import json
import re

from utils.GetFuncUtil import GetFuncUtil


class ReplaceYaml:
    
    def replace_yaml_variable(self,yaml_value):
        """解析yaml文件中的变量引用，并将变量引用替换成实际数据
        Args:
            yaml_value (_type_): 读取yaml文件后需要解析和替换的数据
        Returns:
            _type_: _description_
        """
        yaml_value_str = yaml_value if isinstance(yaml_value,str) else json.dumps(yaml_value)
        #统计数据中${}出现次数并循环
        for _ in range(yaml_value_str.count('${')):
            if '${' in yaml_value_str and '}' in yaml_value_str:
                start_index = yaml_value_str.index('${')
                end_index = yaml_value_str.index('}',start_index)
                #根据索引值切片
                find_data = yaml_value_str[start_index:end_index+1]
                #通过正则匹配()-group找出的变量中的函数名和变量值
                match_data = re.match(r'\$\{(\w+)\((.*?)\)\}',find_data)
                if match_data:
                    func_name,func_params = match_data.groups()
                    func_params = func_params.split(',') if func_params else []
                    #使用面向对象的反射getattr调用函数
                    func_data = getattr(GetFuncUtil(),func_name)(*func_params)
                    #使用正则表达式替换原始字符串中引用的变量
                    yaml_value_str = re.sub(re.escape(find_data),str(func_data),yaml_value_str)
            #还原数据，将其转为字典格式
            try:
                yaml_value = json.loads(yaml_value_str)
            except json.JSONDecodeError:
                yaml_value = yaml_value_str
        return yaml_value