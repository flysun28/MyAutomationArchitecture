#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/9 11:19
# comment:
from lib.common.algorithm.cipher import Cipher
from lib.common.session.http.protobuf import ProtoBuf
from lib.common.utils.globals import HTTPJSON_IN
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import auto_renew_sign_string
from lib.interface_biz.http.pay_pass import Pass
from lib.pb_src.python_native import AutoRenewPb_pb2


class AutoRenew:
    def __init__(self):
        pass

    def auto_renew(self):
        tp_rv = Pass().pass_direct_pay()
        r_v = tp_rv[0]
        t_p = tp_rv[1]
        req = {"header": {"version": "1.0", "t_p": t_p, "imei": "", "model": "PCRM00", "apntype": "1",
                          "package": "com.example.pay_demo", "r_v": r_v, "ext": "", "sdkVer": 260, "country": "CN",
                          "currency": "CNY", "openId": "", "brandType": "OPPO", "mobileos": "17", "androidVersion": "29"
                          },
               "transType": "SIGNANDPAY", "renewProductCode": "20310001",
               "signPartnerOrder": RandomOrder(32).random_string(), "type": "alipay", "amount": "100.0",
               "oriAmount": "100.0", "ip": "58.252.5.75", "sign": "",
               "signAgreementNotifyUrl": "http://secure.pay-test3.wanyol.com/notify/receiver", "appId": "",
               "isNeedExpend": "0",
               "basepay": {"channelId": "", "notifyurl": "http://secure.pay-test3.wanyol.com/notify/receiver",
                           "productName": "签约并支付测试", "productDesc": "签约并支付测试", "partnercode": "2031",
                           "appversion": "260", "currencyName": "人民币", "rate": 1.0,
                           "partnerorder": RandomOrder(32).random_string()},
               "screenInfo": "FULL"}
        sign_string = auto_renew_sign_string(
                req['header']['package'], req['basepay']['partnercode'],
                req['signPartnerOrder'], req['renewProductCode'], req['amount'],
                req['signAgreementNotifyUrl'])
        req['sign'] = Cipher(sign_string).cipher()
        response = ProtoBuf(AutoRenewPb_pb2).runner(HTTPJSON_IN.prefix + '/plugin/post/autorenew', 'Request', req,
                                                    flag=0)
        result = ProtoBuf(AutoRenewPb_pb2).parser('Result', response)

    def only_sign(self):
        tp_rv = Pass().pass_direct_pay()
        r_v = tp_rv[0]
        t_p = tp_rv[1]
        req = {"header": {"version": "1.0", "t_p": t_p, "imei": "", "model": "PCRM00", "apntype": "1",
                          "package": "com.example.pay_demo", "r_v": r_v, "ext": "", "sdkVer": 260, "country": "CN",
                          "currency": "CNY", "openId": "", "brandType": "OPPO", "mobileos": "17", "androidVersion": "29"},
               "transType": "SIGN", "renewProductCode": "20310001", "signPartnerOrder": RandomOrder(32).random_string(),
               "type": "alipay", "amount": "0.0", "oriAmount": "0.0", "ip": "58.252.5.75", "sign": "",
               "signAgreementNotifyUrl": "http://secure.pay-test3.wanyol.com/notify/receiver", "appId": "",
               "isNeedExpend": "0",
               "basepay": {"channelId": "", "notifyurl": "http://secure.pay-test2.wanyol.com/notify/receiver",
                           "productName": "签约测试", "productDesc": "签约测试", "partnercode": "2031",
                           "appversion": "260", "currencyName": "人民币", "rate": 1.0,
                           "partnerorder": RandomOrder(32).random_string()},
               "screenInfo": "FULL"}
        sign_string = auto_renew_sign_string(
            req['header']['package'], req['basepay']['partnercode'],
            req['signPartnerOrder'], req['renewProductCode'], req['amount'],
            req['signAgreementNotifyUrl'])
        req['sign'] = Cipher(sign_string).cipher()
        response = ProtoBuf(AutoRenewPb_pb2).runner(HTTPJSON_IN.prefix + '/plugin/post/autorenew', 'Request', req,
                                                    flag=0)
        result = ProtoBuf(AutoRenewPb_pb2).parser('Result', response)


if __name__ == '__main__':
    AutoRenew().only_sign()