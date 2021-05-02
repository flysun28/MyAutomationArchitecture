#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/8 17:52
# comment:
from lib.common.algorithm.md5 import md5
from lib.common.utils.globals import GlobalVar
from lib.common_biz.find_key import GetKey
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign, old_wx_auto_renew


class AutoRenew:
    def __init__(self):
        pass

    def auto_renew_out(self):
        """
        向渠道发起扣费接口
        :return:
        """
        case_dict = {
            'agreementNo': '202105025920622336',
            'ssoid': '2076075925',
            'renewProductCode': '727243240001',
            'partnerCode': '72724324',
            'partnerOrder': RandomOrder(32).random_num(),
            'payType': 'wxpay',
            # 元
            'amount': '0.01',
            'currencyName': 'CNY',
            'country': 'CN',
            'subject': '测试商品',
            'desc': 'Default product desc...',
            'notifyUrl': 'http://pay.pay-test.wanyol.com/notify/notify/receiver',
            'apppackage': 'com.coloros.cloud',
            'thirdPartId': '2088112811111403',
            'imei': '',
            'model': '',
            'ip': '',
            'ext': '',
            'subUserId': '00002',
            # 签名未校验
            'sign': '54e272460778bb54ea470c7a3ad60531'
        }
        temp_string = Sign(case_dict).join_asc_have_key() + GetKey(case_dict['partnerCode']).get_key_from_merchant()
        case_dict['sign'] = md5(temp_string)
        GlobalVar.HTTPJSON_IN.post("/plugin/autorenew/autorenewpay", data=case_dict)

    def query_sign(self):
        """
        签约查询
        :return:
        """
        case_dict = {
            "ssoid": "2000071235",
            "renewProductCode": "727243140011",
            "partnerCode": "72724314",
            "currencyName": "CNY",
            "country": "CN",
            "sign": "efe9a9b2d3b058789cdd51ed007e5860"
        }
        GlobalVar.HTTPJSON_IN.post("/plugin/autorenew/querysign", data=case_dict)

    def un_sign(self):
        """
        解约。微信需手动，因签约回调去了生产。支付宝仅可在第一套环境，回调地址在支付宝配置死了。
        支付宝:调用接口解约，支付宝会回调导对应的地址。手动解约，是写死在支付宝侧的
        :return:
        """
        case_dict = {
            'agreementNo': '202105025977694378',
            'ssoid': '2076075925',
            'renewProductCode': '727243240001',
            'partnerCode': '72724324',
            'partnerOrder': RandomOrder(18).business_order(""),
            'payType': 'wxpay',
            'currencyName': 'CNY',
            'country': 'CN',
            'apppackage': '',
            'subUserId': '00001',
            'sign': ''
        }
        temp_string = Sign(case_dict).join_asc_have_key() + GetKey(case_dict['partnerCode']).get_key_from_merchant()
        case_dict['sign'] = md5(temp_string)
        GlobalVar.HTTPJSON_IN.post("/plugin/autorenew/unsign", data=case_dict)

    def old_unsign(self):
        req = {
            "ssoid": "2076064003",
            "country": "CN",
            "partnerOrder": "OCLOUD-UNSIGN" + RandomOrder(20).random_num(),
            "payType": "alipay",
            "partnerCode": "231810428",
            "currencyName": "CNY",
            "agreementNo": "20215302717715435440",
            "apppackage": "com.coloros.cloud",
            "sign": "",
            # "alipayUserId":"2088332393982857"
            "alipayUserId": "2088112811111403"
        }
        temp_string = Sign(req).join_asc_have_key("&key=") + GetKey(req['partnerCode']).get_key_from_merchant()
        req['sign'] = md5(temp_string, to_upper=False)
        GlobalVar.HTTPJSON_IN.post("/plugin/oldautorenew/unsign", data=req)

    def wxpayavoidpay(self):
        """
        云服务老的代扣接口-微信
        :return:
        """
        req = {
            "t_p": "", "payorderid": "", "subject": "云服务空间购买", "desc": "云服务空间购买",
            "requestid": "OCLOUD" + RandomOrder(20).random_num() + "AUTO", "paytype": "", "amount": "0.01", "channelid": "", "notifyUrl": "https://aocloud.oppomobile.com/pay/v1/payNotify.json",
            "partnercode": "247628518", "appversion": "", "currencyName": "", "rate": "1", "imei": "", "model": "",
            "apppackage": "com.coloros.cloud", "mac": "", "sdkversion": "", "ip": "", "payVersion": "", "bankNo": "", "bankNm": "", "token": "", "isNeedExpend": "0",
            "ssoid": "2076064003", "payTypeRMBType": "", "type": "", "cardno": "", "cardpwd": "", "ext": "", "requestModel": "", "code": "", "mobile": "", "payrequestidOrder": "", "oriAmount": "", "ext1": "",
            "ext2": "202105025701133124",
            "sign": "", "showUrl": "", "discountInfo": ""
        }
        req['sign'] = md5(old_wx_auto_renew(req, "8m7djj32948d4ad6d822dxda12"), to_upper=False)
        GlobalVar.HTTPJSON_IN.post("/plugin/post/wxpayavoidpay", data="hai"+str(req)+"g")

    def alipayavoidpay(self):
        """
        云服务老的代扣接口-支付宝
        :return:
        """
        req = {
            "t_p": "", "payorderid": "",  "subject": "云服务空间购买", "desc": "云服务空间购买",
            "requestid": "OCLOUD" + RandomOrder(20).random_num() + "AUTO", "paytype": "",
            "amount": "0.01", "channelid": "", "notifyUrl": "https://aocloud.oppomobile.com/pay/v1/payNotify.json",
            "partnercode": "231810428", "appversion": "", "currencyName": "", "rate": "1", "imei": "", "model": "",
            "apppackage": "com.coloros.cloud", "mac": "", "sdkversion": "", "ip": "", "payVersion": "", "bankNo": "", "bankNm": "", "token": "", "isNeedExpend": "0",
            "ssoid": "2076064003", "payTypeRMBType": "", "type": "", "cardno": "", "cardpwd": "", "ext": "", "requestModel": "", "code": "", "mobile": "", "payrequestidOrder": "", "oriAmount": "", "ext1": "",
            "ext2": "{\"ALIPAY_USER_ID\":\"2088112811111403\",\"AGREEMENT_NO\":\"20215302717715435440\"}",
            "sign": "", "showUrl": "", "discountInfo": ""
        }
        req['sign'] = md5(old_wx_auto_renew(req, "8m7djj32948d4ad6d822dxda12"), to_upper=False)
        GlobalVar.HTTPJSON_IN.post("/plugin/post/alipayavoidpay", data="hai"+str(req)+"g")


if __name__ == '__main__':
    flag = "2"
    if flag == "1":
        AutoRenew().auto_renew_out()
    if flag == "2":
        AutoRenew().un_sign()
    if flag == "3":
        AutoRenew().old_unsign()
    if flag == "4":
        AutoRenew().wxpayavoidpay()
    if flag == "5":
        AutoRenew().alipayavoidpay()
