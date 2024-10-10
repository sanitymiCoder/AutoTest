class AssertExceptUtil(Exception):
    """yaml文件断言模式异常"""
    def __init__(self, message="暂不支持该断言模式") -> None:
        self.message = message
        super().__init__(self.message)
        
class RequestExceptUtil(Exception):
    """接口请求访问异常"""
    def __init__(self, message="接口请求访问异常") -> None:
        self.message = message
        super().__init__(self.message)