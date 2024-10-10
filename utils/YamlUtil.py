import random
import re
import yaml
from utils.SetFilePath import FILE_PATH
from utils.HandleLogs import logs

class YamlUtil():
           
    def read_yaml(self,yaml_path):
        """读取yaml文件
        Args:
            yaml_path (_type_): _description_ 文件路径
        Returns:
            _type_: _description_
        """
        try:
            case_list = []
            with open(yaml_path,'r',encoding='utf-8') as f:
                result = yaml.safe_load(f)
                if len(result) <= 1:
                    yaml_data = result[0]
                    base_info = yaml_data.get('baseInfo')
                    for ts in yaml_data.get('caseInfo'):
                        case_info = [base_info,ts]
                        case_list.append(case_info)
                    return case_list
                else: 
                    return result
        except yaml.YAMLError as e:
            logs.error(f'读取yaml文件失败，请检查文件格式，-{e}')
        except UnicodeDecodeError:
            logs.error(f'{yaml_path}文件格式异常,请确认yaml文件编码格式为utf-8!')
        except Exception as e:
            logs.error(f'{yaml_path}文件读取异常，原因：{e}')
            
            
    def write_yaml(self,data,yaml_path=FILE_PATH['extract']):
        """写入yaml文件，一般默认写入extract文件
        Args:
            data (_type_): _description_ 需要写入的数据，字典格式
        """
        try:
            if isinstance(data,dict):
                with open(yaml_path, "a", encoding="utf-8") as f:
                    yaml.dump(data=data,stream=f,allow_unicode=True,sort_keys=False)
            else:
                logs.debug('写入yaml的数据不是字典类型！')
        except Exception as e:
            logs.error(f'写入yaml文件出现异常，原因：{e}')

    
    def clear_yaml(self,yaml_path=FILE_PATH['extract']):
        """清空yaml文件
        Args:
            yaml_path (_type_): _description_ 需要清除内容的yaml文件路径
        """
        with open(yaml_path, "w", encoding="utf-8") as f:
            f.truncate()

            
    def read_extract_yaml(self,first_name,out_format=None):
        """读取extract文件
        Args:
            first_name (_type_): _description_
            out_format (_type_, optional): _description_. Defaults to None.
        Returns:
            _type_: _description_
        """
        yaml_path = FILE_PATH['extract']
        try:
            with open(yaml_path,'r',encoding='utf-8') as f:
                extract_data = yaml.safe_load(f)
                if out_format is None:
                    return extract_data[first_name]
                else:
                    return extract_data.get(first_name,{}).get(out_format)
        except yaml.YAMLError as e:
            logs.error(f'读取yaml文件失败，请检查文件格式，-{e}')
        except UnicodeDecodeError:
            logs.error(f'{yaml_path}文件格式异常,请确认yaml文件编码格式为utf-8!')
        except Exception as e:
            logs.error(f'未知异常，-{e}')
            
            
    def get_extract_data(self,first_name,out_format=None):
        """根据参数获取extract文件中对应的key值
        Args:
            first_name : yaml文件最上层key
            out_format : str类型，0：随机读取；-1：读取全部数据，返回字符串格式；
                        -2：读取全部数据，返回列表格式：其他值按对应顺序读取
        Returns:
            _type_: _description_
        """
        result = self.read_extract_yaml(first_name)
        print(result)
        if out_format is not None and bool(re.compile(r'^[+-]?\d+$').match(str(out_format))):
            out_format = int(out_format)
            data_value = {
                out_format:self.seq_read(result,out_format),
                0 : random.choice(result),
                -1:','.join(result),
                -2:','.join(result).split(',')
             }
            data = data_value[out_format]
        else:
            data = self.read_extract_yaml(first_name,out_format)
        return data
            
            
    def seq_read(self,result,randoms):
        """获取extract返回列表的随机数据
        Args:
            result (_type_): _description_
            randoms (_type_): _description_
        Returns:
            _type_: _description_
        """
        if randoms not in [0,-1,-2]:
            return result[randoms-1]
        else:
            return None

                