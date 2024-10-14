import base64
import hashlib
import hmac
import time
import requests
import urllib
from utils.ConfigParseUtil import ConfigParseUtil

conf =  ConfigParseUtil()
def sign_secret():
    timestamp = str(round(time.time() * 1000))
    #获取钉钉机器人的加签
    secret = conf.get_dingding_value('secret')
    #转码成utf-8
    secret_enc = secret.encode('utf-8')
    #组合当前时间戳和加签密钥
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    #转成byte类型
    string_to_sign_enc = string_to_sign.encode('utf-8')
    #通过加密方式加密当前时间戳和密钥
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp,sign


def send_msg(content,at_all=False):
    """发送钉钉群消息
    Args:
        content (_type_): _description_
        at_all (bool, optional): _description_. Defaults to True.
    """
    timestamp,sign = sign_secret()
    url = conf.get_dingding_value('webhook') + f'&timestamp={timestamp}&sign={sign}'
    headers={'Content-Type':'application/json;charset=UTF-8'}
    data = {'msgtype':'text',
            'text':{
                'content':content,
            },
            'at':{
                'isAtAll':at_all
            }
            }
    res = requests.post(url=url,json=data,headers=headers)
    return res.text