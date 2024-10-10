from utils.YamlUtil import YamlUtil

class GetFuncUtil:
    def get_password(self):
        return "123456"
    
    def get_headers(self):
        headers={
            'Cookies':self.get_cookies(),
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
        return headers
    
    def get_cookies(self):
        cookies = 'session='+YamlUtil().get_extract_data('session')
        return cookies