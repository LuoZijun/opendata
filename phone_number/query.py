#!/usr/bin/env python
#coding: utf8

import random
import re, json
import requests
import sqlite3
import time

"""

官方 查询接口:
    移动: http://www.10086.cn/support/selfservice/ownership/
    联通: http://iservice.10010.com/e3/service/service_belong.html?menuId=000400010003
    电信: http://ah.189.cn/support/common/

"""

conn = sqlite3.connect("data.sqlite3")
cursor = conn.cursor()

def create_database():
    cursor.execute("CREATE TABLE phone_number(pn INTEGER PRIMARY KEY UNIQUE,operator TEXT,network TEXT,sim TEXT,functions TEXT,descp TEXT,source TEXT,ctime INTEGER,utime INTEGER) ")
    conn.commit()

def append(phone_number):
    pass

# 网号 ( 号段 )

# 特殊号段
# 14号段为上网卡专属号段， 中国联通上网卡号段为145，中国移动上网卡号段为147。
# 170号段为虚拟运营商专属号段，170号段的 11 位手机号中前四位用来区分基础运营商，“1700” 为中国电信的转售号码标识，“1705” 为中国移动，“1709” 为中国联通。

# 对于 手机号段当中的 网络制式(GSM/WCDMA/CDMA/TD-SCDMA)，其实没多大作用，因为目前运营商并不限制 某个号段只能使用 某个网络制式,
# 所以这意味着 只要你的手机是支持该网络制式的，那么只要你开通了相关的网络套餐，基本上，2G/3G/4G 你都是可以使用的。
NET_CODE = {
    # 中国移动
    1340: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    1341: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    1342: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    1343: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    1344: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    1345: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    1346: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    1347: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    1348: { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    135:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    136:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    137:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    138:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    139:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    ## 上网卡
    147:  { "operator": "中国移动", "network": "TD-SCDMA/GSM", "Subscriber Identity Module": "USIM/SIM", "functions": "数据卡", "descp": "中国移动香港一卡两号储值卡内地号码" },
    150:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    151:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    152:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    157:  { "operator": "中国移动", "network": "TD-SCDMA", "Subscriber Identity Module": "USIM", "functions": "无线固话卡" },
    158:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    159:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    178:  { "operator": "中国移动", "network": "TD-LTE", "Subscriber Identity Module": "USIM", "functions": "手机卡", "descp": "" },
    182:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    183:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    184:  { "operator": "中国移动", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    187:  { "operator": "中国移动", "network": "TD-SCDMA", "Subscriber Identity Module": "USIM", "functions": "手机卡", "descp": "" },
    188:  { "operator": "中国移动", "network": "TD-SCDMA", "Subscriber Identity Module": "USIM", "functions": "手机卡", "descp": "" },
    # 中国联通
    130:  { "operator": "中国联通", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    131:  { "operator": "中国联通", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    132:  { "operator": "中国联通", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    ## 上网卡
    145:  { "operator": "中国联通", "network": "WCDMA", "Subscriber Identity Module": "USIM", "functions": "数据卡", "descp": "" },
    155:  { "operator": "中国联通", "network": "GSM", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "" },
    156:  { "operator": "中国联通", "network": "GSM/WCDMA", "Subscriber Identity Module": "SIM", "functions": "手机卡", "descp": "中港一卡两号(3G)" },
    176:  { "operator": "中国联通", "network": "FDD-LTE/TD-LTE", "Subscriber Identity Module": "USIM", "functions": "手机卡", "descp": "" },
    185:  { "operator": "中国联通", "network": "WCDMA", "Subscriber Identity Module": "USIM", "functions": "手机卡", "descp": "" },
    186:  { "operator": "中国联通", "network": "WCDMA", "Subscriber Identity Module": "USIM", "functions": "手机卡", "descp": "" },
    # 中国电信
    133:  { "operator": "中国电信", "network": "CDMA", "Subscriber Identity Module": "UIM", "functions": "手机卡", "descp": "" },
    1349: { "operator": "中国电信", "network": "卫星", "Subscriber Identity Module": "unknow", "functions": "手机卡", "descp": "" },
    153:  { "operator": "中国电信", "network": "CDMA", "Subscriber Identity Module": "UIM", "functions": "手机卡", "descp": "" },
    177:  { "operator": "中国电信", "network": "FDD-LTE/TD-LTE", "Subscriber Identity Module": "USIM", "functions": "手机卡", "descp": "" },
    180:  { "operator": "中国电信", "network": "CDMA2000", "Subscriber Identity Module": "UIM", "functions": "手机卡", "descp": "" },
    181:  { "operator": "中国电信", "network": "CDMA2000", "Subscriber Identity Module": "UIM", "functions": "手机卡", "descp": "" },
    189:  { "operator": "中国电信", "network": "CDMA2000", "Subscriber Identity Module": "UIM", "functions": "手机卡", "descp": "" },
    # 虚拟运营商
    1700:  { "operator": "中国电信", "network": "unknow", "Subscriber Identity Module": "UIM", "functions": "手机卡", "descp": "" },
    1705:  { "operator": "中国移动", "network": "unknow", "Subscriber Identity Module": "USIM", "functions": "手机卡", "descp": "" },
    1709:  { "operator": "中国联通", "network": "unknow", "Subscriber Identity Module": "USIM", "functions": "手机卡", "descp": "" },

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
        if int(result['status']) == 1 and int(result['pn']) == int(phone_number):
            # for k in result:
            #     print "%s: %s" % ( k, result[k] )
            info = {
                "pn": int(result['pn']), 
                "province_name": result['ProvName'],
                "city_name": result['CityName']
            }
            print str(info)
            return info
        else:
            return None

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
        # print u"searchIndex: %s" % result['searchIndex']

        if "dto" in result and result['dto'] != None and int(result['dto']['beginMobile']) == int(phone_number):
            #print result['dto']
            #for k in result['dto']:
            #    print "%s: %s" % ( k, result['dto'][k] )
            info = {
                "pn": int(result['dto']['beginMobile']), 
                "province_name": result['dto']['provinceName'],
                "city_name": result['dto']['cityName']
            }
            print str(info)
            return info
        else:
            # print u"**查询失败."
            return None

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

"""
import requests, re
try:
    from bs4 import BeautifulSoup
except:
    from BeautifulSoup import BeautifulSoup


def query(mobile_id):
	print u"Query: %s 运营商: 联通" % str(mobile_id)
	url = "http://wap.10010.com/t/customerService/queryAffiliationPlace.htm?desmobile=&version="
	payload = {"mobile_id": str(mobile_id) }
	r = requests.post(url, data=payload)
	if r.status_code != 200:
		print u"ERROR \t %s " % mobile_id
	DOM = BeautifulSoup(r.content, 'html.parser')
	if len(DOM.find_all('td')) == 0:
		print u"\tWARN: 数据不存在."
		return False
	values = map(lambda elem: unicode(elem.find('span').get_text()), DOM.find_all('td'))
	print '\tResult: ' + '\t'.join(values) + '\n'

query('18516540691')
query('18702159534')


""""
def main():
    q = ChinaMobile()
    # q = ChinaUnicom()
    code = "1340"
    b = 0
    while b < 100000:
        bb = "0"*(8+(3-len(code))-len(str(b))) + str(b)
        if len( code+bb ) == 11:
            info = q.query( code + bb)
            if info == None:
                open("no_response.log", "a").write( str(time.time()) + "\t" + code+bb + "\n" )
            else:
                open("result.log", "a").write( json.dumps(info) + "\n" )
        else:
            print "手机号码长度错误"
            open("error.log", "a").write( str(time.time()) + "\t" +code + "\t" + bb + "\t长度错误")
        b += 1

if __name__ == '__main__':
    main()
    # create_database()
