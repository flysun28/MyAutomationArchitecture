#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/25 16:04
# comment:
from lib.common.session.http.protobuf import ProtoBuf
from lib.common.utils.globals import GlobarVar, HTTPJSON_OUT
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.replace_parameter import ReplaceParams
from lib.pb_src.python_standard import Spend_pb2


class Spend:
    def __init__(self, pay_amount, priceLocal, version="15.0", partner_id="2031", country="VN", currency="VND"):
        self.version = version
        self.partner_id = partner_id
        self.country = country
        # 元
        self.pay_amount = str(pay_amount)
        self.priceLocal = str(priceLocal)
        self.currency = currency

    def kb_spend(self):
        req = {
            "header": {
                "version": self.version,
                "token": "",
                "imei": "",
                "model": "A001OP",
                "apntype": "1",
                "package": "com.example.pay_demo",
                "r_v": "",
                "sign": "",
                "sdkVer": "12.0",
                "appVerison": "",
                "ip": "0.0.0.0",
                "openId": "FBC4E853B36C40C8A2AC61D127D85C9E23fe8cbbef964f0009fa0ac296d07836",
                "brandType": "OPPO",
                "mobileos": "17",
                "androidVersion": "29"
            },
            "partnerOrder": RandomOrder(32).random_string(),
            "partnerId": "2031",
            "country": self.country,
            "payType": "cocoin",
            "channel": "cocoin",
            "payAmount": self.pay_amount,
            "currency": self.currency,
            "product": {
                "name": "ONLY_KB_SPEND",
                "desc": "ONLY_KB_SPEND",
                "count": "1",
                "priceLocal": self.pay_amount
            },
            "returnUrl": "",
            "notifyUrl": str(GlobarVar.URL_PAY_IN) + "/notify/receiver",
            "partnerParams": "",
            "extendParams": "",
            "businessType": "WANGYOU",
            "businessChannelId": "",
            "factor": ""
        }
        ReplaceParams(req).replace_standard("expend")
        response = ProtoBuf(Spend_pb2).runner(HTTPJSON_OUT.prefix + '/plugin/spend', 'SpendRequest', req)
        result = ProtoBuf(Spend_pb2).parser('SpendResult', response)

    def kb_vou_spend(self, couponId, discountAmount):
        # discountAmount + pay_amount = priceLocal
        req = {
            "header": {
                "version": self.version,
                "token": "",
                "imei": "",
                "model": "A001OP",
                "apntype": "1",
                "package": "com.example.pay_demo",
                "r_v": "",
                "sign": "",
                "sdkVer": "12.0",
                "appVerison": "",
                "ip": "0.0.0.0",
                "openId": "FBC4E853B36C40C8A2AC61D127D85C9E23fe8cbbef964f0009fa0ac296d07836",
                "brandType": "OPPO",
                "mobileos": "17",
                "androidVersion": "29"
            },
            "partnerOrder": "",
            "partnerId": self.partner_id,
            "country": self.country,
            "payType": "cocoin",
            "channel": "cocoin",
            "payAmount": self.pay_amount,
            "currency": self.currency,
            "product": {
                "name": "KB_VOU_SPEND",
                "desc": "KB_VOU_SPEND",
                "count": "1",
                "priceLocal": self.priceLocal
            },
            "returnUrl": "",
            "notifyUrl": "http://pay.pay-test.wanyol.com/notify/receiver",
            "partnerParams": "",
            "extendParams": "",
            "businessType": "WANGYOU",
            "businessChannelId": "",
            "couponId": str(couponId),
            "discountAmount": str(discountAmount),
            "factor": ""
        }
        ReplaceParams(req).replace_standard("expend")
        response = ProtoBuf(Spend_pb2).runner(HTTPJSON_OUT.prefix + '/plugin/spend', 'SpendRequest', req)
        result = ProtoBuf(Spend_pb2).parser('SpendResult', response)


if __name__ == '__main__':
    Spend(1000, 1000).kb_spend()
    Spend(1001, 2000).kb_vou_spend(1213222, 999)
