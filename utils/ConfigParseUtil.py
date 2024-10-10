import configparser
from utils.SetFilePath import FILE_PATH

class ConfigParseUtil():
    
    def __init__(self,file_path = FILE_PATH['config']) -> None:
        self.file_path = file_path
        self.config = configparser.ConfigParser()
        self.config.read(self.file_path)
        
    def get_value(self,section,option):
        try:
            return self.config.get(section,option)
        except Exception as e:
            print(f'读取配置文件出现异常，原因:{e}')
            
    def get_env_value(self,option):
        try:
            return self.get_value('ENV',option)
        except Exception as e:
            print(f'读取配置文件出现异常，原因:{e}')
            
    def get_db_value(self,option):
        try:
            return self.get_value('MYSQL',option)
        except Exception as e:
            print(f'读取配置文件出现异常，原因:{e}')