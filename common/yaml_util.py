import os

import yaml


class YamlUtil(object):

    #读取yaml文件
    def read_extract_yaml(self,key):
        with open(os.getcwd()+"/extract.yml",mode="r",encoding="utf-8") as f:
            value = yaml.load(stream=f,Loader=yaml.FullLoader)
            return value[key]

    # 写入yaml文件
    def write_extract_yaml(self,data):
        with open(os.getcwd() + "/extract.yml", mode="a", encoding="utf-8") as f:
            yaml.dump(data=data,stream=f,allow_unicode=True)

    #清除yaml文件
    def clear_extract_yaml(self):
        with open(os.getcwd() + "/extract.yml", mode="w", encoding="utf-8") as f:
            f.truncate()


    #读取用例yaml文件
    def read_testcase_yaml(self,yamlname):
        with open(os.getcwd()+"/testcases/"+yamlname,mode="r",encoding="utf-8") as f:
            value = yaml.load(stream=f,Loader=yaml.FullLoader)
            return value

