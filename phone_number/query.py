#!/usr/bin/env python
#coding: utf8

import random
import re, json
import requests
"""

官方 查询接口:
    移动: http://www.10086.cn/support/selfservice/ownership/
    联通: http://iservice.10010.com/e3/service/service_belong.html?menuId=000400010003
    电信: http://ah.189.cn/support/common/

"""
# 网号 ( 号段 )

# 特殊号段
# 14号段为上网卡专属号段， 中国联通上网卡号段为145，中国移动上网卡号段为147。
# 170号段为虚拟运营商专属号段，170号段的 11 位手机号中前四位用来区分基础运营商，“1700” 为中国电信的转售号码标识，“1705” 为中国移动，“1709” 为中国联通。

# 对于 手机号段当中的 网络制式(GSM/WCDMA/CDMA/TD-SCDMA)，其实没多大作用，因为目前运营商并不限制 某个号段只能使用 某个网络制式,
# 所以这意味着 只要你的手机是支持该网络制式的，那么只要你开通了相关的网络套餐，基本上，2G/3G/4G 你都是可以使用的。
NET_CODE = {
    # 中国移动
    1340: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    1341: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    1342: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    1343: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    1344: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    1345: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    1346: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    1347: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    1348: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    135:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    136:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    137:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    138:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    139:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    ## 上网卡
    147:  { "operator": "中国移动", "network": "TD-SCDMA/GSM", "Subscriber Identity Module": "USIM/SIM", "functions": "数据卡", "descp": "中国移动香港一卡两号储值卡内地号码" },
    150:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    151:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    152:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    157:  { "operator": "中国移动", "network": "TD-SCDMA", "Subscriber Identity Module": "USIM", "functions": "无线固话卡" },
    158:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    159:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    178:  { "operator": "中国移动", "network": "TD-LTE", "Subscriber Identity Module": "USIM", "functions": "手机卡" },
    182:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    183:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    184:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    187:  { "operator": "中国移动", "network": "TD-SCDMA", "Subscriber Identity Module": "USIM", "functions": "手机卡" },
    188:  { "operator": "中国移动", "network": "TD-SCDMA", "Subscriber Identity Module": "USIM", "functions": "手机卡" },
    # 中国联通
    130:  { "operator": "中国联通", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    131:  { "operator": "中国联通", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    132:  { "operator": "中国联通", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    ## 上网卡
    145:  { "operator": "中国联通", "network": "WCDMA", "Subscriber Identity Module": "USIM", "functions": "数据卡" },
    155:  { "operator": "中国联通", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡" },
    156:  { "operator": "中国联通", "network": "GSM/WCDMA", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "中港一卡两号(3G)" },
    176:  { "operator": "中国联通", "network": "FDD-LTE/TD-LTE", "Subscriber Identity Module": "USIM", "functions": "手机卡" },
    185:  { "operator": "中国联通", "network": "WCDMA", "Subscriber Identity Module": "USIM", "functions": "手机卡" },
    186:  { "operator": "中国联通", "network": "WCDMA", "Subscriber Identity Module": "USIM", "functions": "手机卡" },
    # 中国电信
    133:  { "operator": "中国电信", "network": "CDMA", "Subscriber Identity Module": "UIM", "functions": "手机卡" },
    1349: { "operator": "中国电信", "network": "卫星", "Subscriber Identity Module": "unknow", "functions": "手机卡" },
    153:  { "operator": "中国电信", "network": "CDMA", "Subscriber Identity Module": "UIM", "functions": "手机卡" },
    177:  { "operator": "中国电信", "network": "FDD-LTE/TD-LTE", "Subscriber Identity Module": "USIM", "functions": "手机卡" },
    180:  { "operator": "中国电信", "network": "CDMA2000", "Subscriber Identity Module": "UIM", "functions": "手机卡" },
    181:  { "operator": "中国电信", "network": "CDMA2000", "Subscriber Identity Module": "UIM", "functions": "手机卡" },
    189:  { "operator": "中国电信", "network": "CDMA2000", "Subscriber Identity Module": "UIM", "functions": "手机卡" },
    # 虚拟运营商
    1700:  { "operator": "中国电信", "network": "unknow", "Subscriber Identity Module": "UIM", "functions": "手机卡" },
    1705:  { "operator": "中国移动", "network": "unknow", "Subscriber Identity Module": "USIM", "functions": "手机卡" },
    1709:  { "operator": "中国联通", "network": "unknow", "Subscriber Identity Module": "USIM", "functions": "手机卡" },

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
        print u"searchIndex: %s" % result['searchIndex']

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
    q = ChinaMobile()
    # q = ChinaUnicom()
    q.query("18602730947")
    q.query("15391565549")

if __name__ == '__main__':
    main()