#!/usr/bin/env python
#coding: utf8

import random
import re, json
import requests, urllib
"""

官方 查询接口:
    移动: http://www.10086.cn/support/selfservice/ownership/
    联通: http://iservice.10010.com/e3/service/service_belong.html?menuId=000400010003
    电信: http://ah.189.cn/support/common/

"""


class ChinaMobile:
    "检索中国移动网络"
    requests = None
    verify_code = ""
    def __init__ (self):
        self.mk_session()
    def mk_session(self):
        self.requests = requests.Session()
        r = self.requests.get("http://www1.10086.cn/jsp/common/image.jsp?r=0.7038094939198345")
        open("verify.jpg", "wb").write(r.content)
        self.verify_code = raw_input("请输入验证码: ")
    def query(self, phone_number):
        print "========检索移动数据库: %s ========" % str(phone_number)
        url = "http://www1.10086.cn/service/shop/attributionwithcode.jsp"
        payload = {"pn": str(phone_number), "verify": self.verify_code, "callback": "jsoncallback", "_": random.random() }
        r = self.requests.get( url, params=payload );
        body = re.compile(r"jsoncallback\(\n(.*?)\n\)", re.DOTALL).findall(r.text)[0]
        """
            {
                u'status': u'1', 
                u'ProvName': u'\u6e56\u5317', 
                u'ProvId': u'270', 
                u'CityName': u'\u6b66\u6c49', 
                u'CityId': u'270', 
                u'pn': u'18602730947'
            }
        """
        result = json.loads(body)
        #print result
        for k in result:
            print "%s: %s" % ( k, result[k] )
        

class ChinaUnicom:
    "检索中国联通网络"
    requests = None
    verify_code = None
    def __init__(self):
        self.mk_session()
    def mk_session(self):
        self.requests = requests.Session()
    def query(self, phone_number):
        print "========检索联通数据库: %s =========" % str(phone_number)

        url = "http://iservice.10010.com/e3/static/life/callerLocationQuery?_=" + str(random.random())
        data = {"number": phone_number, "checkCode": self.verify_code}
        r = self.requests.post( url, data=data )
        result = json.loads(r.text)
        """
        {
            u'isSuccess': True, 
            u'validateflag': True, 
            u'searchIndex': 2, 
            u'dto': {
                u'cityCode': u'710', 
                u'provinceName': u'\u6e56\u5317', 
                u'areaCode': u'027', 
                u'cityName': u'\u6b66\u6c49', 
                u'provinceCode': u'071', 
                u'endMobile': u'18602739999', 
                u'mobileLength': u'7', 
                u'id': u'8a0e248a4efd4a4c014f008b3c411772', 
                u'beginMobile': u'18602730000'
            }
        }
        """
        if "dto" in result and result['dto'] != None:
            #print result['dto']
            for k in result['dto']:
                print "%s: %s" % ( k, result['dto'][k] )
        else:
            print u"**查询失败."

class ChinaTelecom:
    "检索中国电信服务"
    requests = None
    verify_code = None
    def __init__(self):
        pass
    def mk_session(self):
        self.requests = requests.Session()
    def query(self, phone_number):
        url = "http://ah.189.cn/support/common/"



def main():
    # q = ChinaMobile()
    q = ChinaUnicom()
    q.query("18602730947")
    q.query("15391565549")

if __name__ == '__main__':
    main()