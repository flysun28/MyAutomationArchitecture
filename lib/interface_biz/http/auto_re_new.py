#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/20 9:48
# comment:

from lib.common.algorithm.cipher import Cipher
from lib.common.session.http.protobuf import ProtoBuf
from lib.common.utils.globals import HTTPJSON_IN, GlobalVar
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import auto_renew_sign_string
from lib.interface_biz.http.pay_pass import Pass
from lib.pb_src.python_native import AutoRenewPb_pb2


class AutoRenew:
    def __init__(self, pay_type, partner_code, version, app_version, renewProductCode, notify_url):
        self.version = version
        self.renewProductCode = renewProductCode
        self.partner_code = partner_code
        self.app_version = app_version
        self.type = pay_type
        self.notify_url = notify_url

    def auto_renew(self, amount):
        """
        :param amount: 传分，接口传入为元 /100处理
        :return:
        """
        tp_rv = Pass().pass_direct_pay()
        r_v = tp_rv[0]
        t_p = tp_rv[1]
        partner_order = RandomOrder(32).random_string()
        req = {"header": {"version": self.version, "t_p": t_p, "imei": "", "model": "PCRM00", "apntype": "1",
                          "package": "com.example.pay_demo", "r_v": r_v, "ext": "", "sdkVer": 260, "country": "CN",
                          "currency": "CNY", "openId": "", "brandType": "OPPO", "mobileos": "17", "androidVersion": "29"
                          },
               "transType": "SIGNANDPAY", "renewProductCode": self.renewProductCode,
               "signPartnerOrder": partner_order, "type": self.type, "amount": str(amount/100),
               "oriAmount": str(amount/100), "ip": "58.252.5.75", "sign": "",
               "signAgreementNotifyUrl": self.notify_url, "appId": "",
               "isNeedExpend": "0",
               "basepay": {"channelId": "", "notifyurl": self.notify_url,
                           "productName": "SIGN_PAY", "productDesc": "SIGN_PAY", "partnercode": self.partner_code,
                           "appversion": self.app_version, "currencyName": "人民币", "rate": 1.0,
                           "partnerorder": partner_order},
               "screenInfo": "FULL"}
        sign_string = auto_renew_sign_string(
                req['header']['package'], req['basepay']['partnercode'],
                req['signPartnerOrder'], req['renewProductCode'], req['amount'],
                req['signAgreementNotifyUrl'])
        req['sign'] = Cipher(sign_string).cipher()
        response = ProtoBuf(AutoRenewPb_pb2).runner(HTTPJSON_IN.prefix + '/plugin/post/autorenew', 'Request', req,
                                                    flag=0)
        result = ProtoBuf(AutoRenewPb_pb2).parser('Result', response)
        return {"pay_req_id": result.payrequestid, "partner_code": req['basepay']['partnerorder']}

    def only_sign(self):
        tp_rv = Pass().pass_direct_pay()
        r_v = tp_rv[0]
        t_p = tp_rv[1]
        partner_order = RandomOrder(32).random_string()
        req = {"header": {"version": self.version, "t_p": t_p, "imei": "", "model": "PCRM00", "apntype": "1",
                          "package": "com.example.pay_demo", "r_v": r_v, "ext": "", "sdkVer": 260, "country": "CN",
                          "currency": "CNY", "openId": "", "brandType": "OPPO", "mobileos": "17", "androidVersion": "29"
                          },
               "transType": "SIGN", "renewProductCode": self.renewProductCode,
               "signPartnerOrder": partner_order, "type": self.type, "amount": "0.0",
               "oriAmount": "0.0", "ip": "58.252.5.75", "sign": "",
               "signAgreementNotifyUrl": self.notify_url, "appId": "",
               "isNeedExpend": "0",
               "basepay": {"channelId": "", "notifyurl": self.notify_url,
                           "productName": "ONLY_SIGN", "productDesc": "ONLY_SIGN", "partnercode": self.partner_code,
                           "appversion": self.app_version, "currencyName": "人民币", "rate": 1.0,
                           "partnerorder": partner_order},
               "screenInfo": "FULL"}
        sign_string = auto_renew_sign_string(
            req['header']['package'], req['basepay']['partnercode'],
            req['signPartnerOrder'], req['renewProductCode'], req['amount'],
            req['signAgreementNotifyUrl'])
        req['sign'] = Cipher(sign_string).cipher()
        response = ProtoBuf(AutoRenewPb_pb2).runner(HTTPJSON_IN.prefix + '/plugin/post/autorenew', 'Request', req,
                                                    flag=0)
        result = ProtoBuf(AutoRenewPb_pb2).parser('Result', response)
        return {"pay_req_id": result.payrequestid, "partner_code": req['basepay']['partnerorder']}


if __name__ == '__main__':
    AutoRenew().only_sign()