#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/24 19:54
# comment:
from lib.common.session.http.protobuf import ProtoBuf
from lib.common.utils.globals import HTTPJSON_OUT, GlobarVar
from lib.common.utils.meta import WithLogger
from lib.common_biz.replace_parameter import ReplaceParams
from lib.interface_biz.scarlett.upay import upay_pay_scarlet
from lib.pb_src.python_standard import RechargeAndSpend_pb2


class RechargeSpend(metaclass=WithLogger):
    def __init__(self, pay_amount, pay_type="upay_gamecard", country="VN", currency="VND", partner_id="2031",
                 app_version="250", version="15.0"):
        self.version = version
        self.app_version = app_version
        self.partner_id = partner_id
        self.country = country
        # 元
        self.pay_amount = pay_amount
        self.currency = currency
        self.pay_type = pay_type

    def recharge_spend_price_is_amount(self):
        """
        商品金额=支付金额，不带券不带可币
        :return:
        """
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
                "appVerison": self.app_version,
                "ip": "0.0.0.0",
                "openId": "FBC4E853B36C40C8A2AC61D127D85C9E23fe8cbbef964f0009fa0ac296d07836",
                "brandType": "OPPO",
                "mobileos": "17",
                "androidVersion": "29"
            },
            "partnerOrder": "",
            "partnerId": self.partner_id,
            "country": self.country,
            "payType": self.pay_type,
            "channel": self.pay_type,
            "payAmount": self.pay_amount,
            "currency": self.currency,
            "cocoinRechargeAmount": "",
            "cocoinPayAmount": "0.0",
            "product": {
                "name": "RECHARGE_SPEND",
                "desc": "RECHARGE_SPEND",
                "priceLocal": self.pay_amount
            },
            "notifyUrl": str(GlobarVar.URL_PAY_IN)+"/notify/receiver",
            "partnerParams": "",
            "businessChannelId": "",
            "factor": ""
        }
        ReplaceParams(req).replace_standard("expend")
        response = ProtoBuf(RechargeAndSpend_pb2).runner(HTTPJSON_OUT.prefix + '/plugin/cocoin/recharge/spend',
                                                         'RechargeAndSpendRequest', req, flag=1)
        result = ProtoBuf(RechargeAndSpend_pb2).parser('RechargeAndSpendResponse', response)
        # upay_pay_scarlet(10000, result.data.payRequestId)


if __name__ == '__main__':
    RechargeSpend("100").recharge_spend_price_is_amount()
