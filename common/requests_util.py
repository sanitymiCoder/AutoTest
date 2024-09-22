import json

import requests


class RequestsUtil:
    session = requests.session()

    def send_requests(self,method,url,data=None,**kwargs):
        method = method.upper()
        resp = None
        if method == "GET":
            resp = RequestsUtil().session.request(method,url,params=data,**kwargs)
        if method == "POST":
            resp = RequestsUtil().session.request(method,url,json=data,**kwargs)
        return resp.text
