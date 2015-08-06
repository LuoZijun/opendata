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

CompanyCode = {
    "ChinaMobile": [
        1340, 1341, 1342, 1343, 1344, 1345 ,1346, 1347, 1348,  # GSM SIM手机卡
        135, 136, 137, 138, 139, # GSM SIM手机卡
        147, # TD-SCDMA/GSM    USIM/SIM数据卡 / 中国移动香港一卡两号储值卡内地号码
        150, 151, 152, 157, 158, 159, # GSM SIM手机卡 ( 157 为 TD-SCDMA    USIM无线固话卡 )
        178, # TD-LTE  USIM手机卡
        182, 183, 184, 187, 188  # GSM SIM手机卡 (  187 & 188 为 TD-SCDMA    USIM手机卡 )
    ],
    "ChinaUnicom": [
        130, 131, 132, # GSM SIM手机卡
        145,   # WCDMA   USIM数据卡
        155, 156,  # 155: GSM SIM手机卡,  156: GSM/WCDMA   SIM手机卡/中港一卡两号(3G)
        176,  # FDD-LTE/TD-LTE  USIM手机卡
        185, 186 # WCDMA   USIM手机卡
    ],
    "ChinaTelecom": [
        133,     # CDMA    UIM手机卡
        1349,   # 卫星手机卡
        153,     # CDMA    UIM手机卡
        177,     # FDD-LTE/TD-LTE  USIM手机卡
        180, 181, 189 # CDMA2000    UIM手机卡
    ],
    "NetCard": [ 14 ],  # 14号段为上网卡专属号段， 中国联通上网卡号段为145，中国移动上网卡号段为147。
    "VirtualCompany": [170]
}

# 14号段为上网卡专属号段， 中国联通上网卡号段为145，中国移动上网卡号段为147。
NetCard = {
    "ChinaUnicom": [145],
    "ChinaMobile": [147]
}

# 170号段为虚拟运营商专属号段，170号段的 11 位手机号中前四位用来区分基础运营商，
#  “1700” 为中国电信的转售号码标识，“1705” 为中国移动，“1709” 为中国联通。
VirtualCompany = {
    "ChinaTelecom": [ 1700 ],   # UIM手机卡
    "ChinaMobile": [1705],        # USIM手机卡
    "ChinaUnicom": [1709],       # USIM手机卡
}

def where_are_you_from (phone_number):
    # 判断 手机号码 所属的运营商
    pass

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