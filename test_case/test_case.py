import re

import requests


class TestCase(object):
    token = ""
    cookie = ""
    session = requests.session()

    def test_login(self):
        url='http://localhost/base/login'
        data={
            "username":"admin",
            "password":"123456"
        }
        resp = TestCase.session.post(url=url,json=data)
        TestCase.token = resp.json()['token']
        TestCase.cookie = re.match("(.*?)Http",resp.headers.get("Set-Cookie"))[1]
        print(resp.json())

    def test_getInfo(self):
        url='http://localhost/base/getInfo'
        # headers = {'authorization':'Bearer '+TestCase.token,
        #            # 'cookie':TestCase.cookie+'Admin-Token='+TestCase.token
        #            }
        resp = TestCase.session.get(url=url)
        print(resp.json())


    def test_getRouters(self):
        url='http://localhost/base/getRouters'
        # headers = {'authorization':'Bearer '+TestCase.token,
        #            # 'cookie':TestCase.cookie+'Admin-Token='+TestCase.token
        #            }
        resp = TestCase.session.get(url=url)
        print(resp.json())

    def test_loginOut(self):
        url='http://localhost/base/logout'
        # headers = {'authorization':'Bearer '+TestCase.token,
        #            # 'cookie':TestCase.cookie+'Admin-Token='+TestCase.token
        #            }
        resp = TestCase.session.post(url=url)


