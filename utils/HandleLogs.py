import time
import logging
import os
from utils.SetFilePath import FILE_PATH

logs_path = FILE_PATH['logs']
if not os.path.exists(logs_path):
    os.mkdir(logs_path)

log_name = logs_path + r'\test_{}.log'.format(time.strftime('%Y%m%d-%H_%M_%S'))

class HandleLogs:
    
    def output_logs(self):
        logger = logging.getLogger(__name__)
        #防止重复打印日志
        if not logger.handlers:
            logger.setLevel(logging.DEBUG)
            log_format = logging.Formatter('%(asctime)s-[%(module)s:%(funcName)s]-%(levelname)s-%(message)s')
            #把日志输出到控制台
            sh = logging.StreamHandler()
            sh.setLevel(logging.DEBUG)
            sh.setFormatter(log_format)
            logger.addHandler(sh)
            
            #把日志输出到文件里
            fh = logging.FileHandler(filename=log_name,mode='a',encoding='utf-8')
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(log_format)
            logger.addHandler(fh)
        return logger
    
    def clear_logs():
        # 要删除文件的目录
        directory = './logs'
        # 列出目录下所有文件和文件夹
        files_and_folders = os.listdir(directory)
        # 过滤出所有.log文件
        log_files = [file for file in files_and_folders if file.endswith('.log')]
        # 删除每一个.log文件
        for log_file in log_files:
            file_path = os.path.join(directory, log_file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                
    
handle = HandleLogs()
logs= handle.output_logs()