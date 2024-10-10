import os
import sys

DIR_PATH = os.getcwd()
sys.path.append(DIR_PATH)

#print(DIR_PATH)

FILE_PATH={
    'extract':os.path.join(DIR_PATH,'extract.yaml'),
    'login':os.path.join(DIR_PATH,'data','login.yaml'),
    'getInfo':os.path.join(DIR_PATH,'data','getInfo.yaml'),
    'getRouters':os.path.join(DIR_PATH,'data','getRouters.yaml'),  
    'configList':os.path.join(DIR_PATH,'data','configList.yaml'),
    'dictList':os.path.join(DIR_PATH,'data','dictList.yaml'),
    'userEdit':os.path.join(DIR_PATH,'data','userEdit.yaml'),
    'userList':os.path.join(DIR_PATH,'data','getUserList.yaml'),
    'fileUpload':os.path.join(DIR_PATH,'data','fileUpload.yaml'),
    'deptList':os.path.join(DIR_PATH,'data','deptList.yaml'),
    'business':os.path.join(DIR_PATH,'data','business.yaml'),
    
    'config':os.path.join(DIR_PATH,'configs','config.ini'),
    'logs':os.path.join(DIR_PATH,'logs')
}