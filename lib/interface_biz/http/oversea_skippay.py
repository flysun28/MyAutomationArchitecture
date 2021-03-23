#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/25 22:00
# comment:
from lib.common.session.http.protobuf import ProtoBuf
from lib.common.utils.globals import HTTPJSON_OUT, GlobalVar
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.replace_parameter import ReplaceParams
from lib.pb_src.python_standard import SkipPay_pb2


class Skippay:
    def __init__(self, payAmount, priceLocal, version, partner_id, country, currency, payType):
        self.version = version
        self.partner_id = partner_id
        self.country = country
        # 元
        self.payAmount = str(payAmount)
        self.priceLocal = str(priceLocal)
        self.currency = currency
        self.payType = payType

    def skip_pay(self, isLogin=""):
        """
        1. 无账号支付 token='' , r_v='RvDf0ABC'
        2. 有账号支付 token与r_v正常传
        :return:
        """
        req = {
            "header": {
                "version": self.version,
                "token": isLogin,
                "imei": "",
                "model": "CPH2179",
                "apntype": "1",
                "package": "com.example.pay_demo",
                "r_v": "",
                "sign": "",
                "sdkVer": "12.0",
                "appVerison": "250",
                "ip": "0.0.0.0",
                "openId": "278CBA1874A7489EAAA94585CCE9F8180f6aaceaf8b3cb179539d5dbb51e8a69",
                "brandType": "OPPO",
                "mobileos": "18",
                "androidVersion": "29"
            },
            "partnerOrder": RandomOrder(32).random_string(),
            "partnerId": self.partner_id,
            "country": self.country,
            "payType": self.payType,
            "channel": self.payType,
            "payAmount": self.payAmount,
            "currency": self.currency,
            "product": {
                "name": "SKIP_PAY",
                "desc": "SKIP_PAY",
                "count": "1",
                "priceLocal": self.priceLocal
            },
            "returnUrl": "",
            "notifyUrl": str(GlobalVar.URL_PAY_IN) + "/notify/receiver",
            "partnerParams": "",
            "extendParams": "",
            "businessChannelId": "",
            "bankCode": "",
            "factor": ""
        }
        ReplaceParams(req).replace_standard("no_login")
        response = ProtoBuf(SkipPay_pb2).runner(HTTPJSON_OUT.prefix + '/plugin/skippay', 'SkipPayRequest'
                                                 , req)
        result = ProtoBuf(SkipPay_pb2).parser('SkipPayResponse', response)
        return {"pay_req_id": result.data.payRequestId, "partner_order": req["partnerOrder"]}


if __name__ == '__main__':
    Skippay(500, 500, payType="codapay_store").skip_pay("no_login")
    Skippay(500, 500).skip_pay()
