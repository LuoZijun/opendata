#!/usr/bin/env python
#coding: utf8

import random
import re, json
import requests, urllib
"""
    移动: http://www.10086.cn/support/selfservice/ownership/
    联通: http://iservice.10010.com/e3/service/service_belong.html?menuId=000400010003
    电信: http://ah.189.cn/support/common/



手机号码示例:
    电信: 15391565549
    联通: 18602730947
    移动: 

"""

class Query:
    phone_number = 0
    def __init__(self):
        pass
    def query(self, phone_number):
        # 查询手机号码 ( 三网数据合并 )
        self.phone_number = int(phone_number)
        print self.from_10010()
    def _parse_response(self, r):
        http_code = int(r.status_code)
        try:
            try:
                _http_body = re.compile(r"jsoncallback\(\n(.*?)\n\)", re.DOTALL).findall(r.text)[0]
            except:
                _http_body = r.text
            http_body = json.loads(_http_body)
        except:
            http_body = r.text
        http_header = r.headers
        #content_type = r.headers['content-type']
        response = { "code": http_code, "headers": None, "body": http_body }
        return response
    def from_10000(self):
        # 检索电信网络
        url = "http://ah.189.cn/support/common/"

    def from_10010(self):
        # 联通号码查询
        # curl -X POST -d "number=18602730947" \
        #      "http://iservice.10010.com/e3/static/life/callerLocationQuery?_=1438767945817"
        url = "http://iservice.10010.com/e3/static/life/callerLocationQuery?_=" + str(random.random())
        data = {"number": self.phone_number, "checkCode": None}
        print "检索联通数据库: %s " % str(data)
        r = requests.post( url, data=data )
        return self._parse_response( r )
    def from_10086(self):
        # 检索 移动网络
        # 对应的 验证码: 979363
        # JSESSIONID: d6ZGVBdJWL2vbQWp4jWpjTQ35V8xGyfh1v802F7HDFJV5vKfgWs8!-1538034262   www1.10086.cn
        # http://www1.10086.cn/service/shop/attributionwithcode.jsp?pn=18602730947&verify=569836&callback=jsoncallback&_=1438768989880
        url = "http://www1.10086.cn/service/shop/attributionwithcode.jsp"
        # pn=18602730947&verify=569836&callback=jsoncallback&_=1438768989880
        payload = {"pn": self.phone_number, "verify": "17d688", "callback": "jsoncallback", "_": random.random() }
        headers = {
            "Cookie": "JSESSIONID=FLJkVBnTp5hsLxv729v9GZhv27cfMdnY1HCJVP4b6KfhMB92T5TB!-1538034262",
            "Host": "www1.10086.cn",
            "Referer": "http://www.10086.cn/support/selfservice/ownership/",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }
        # Request Verify Image ( Method: GET ): http://www1.10086.cn/jsp/common/image.jsp?r=0.7038094939198345 
        # Request Session
        # s = requests.Session()
        print "检索移动数据库: %s " % str(payload)
        r = requests.get( url, params=payload, headers=headers );
        return self._parse_response( r )
def main():
    q = Query()
    q.query(13117025667)

if __name__ == '__main__':
    main()