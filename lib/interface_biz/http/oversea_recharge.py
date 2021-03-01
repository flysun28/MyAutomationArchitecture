#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/25 15:04
# comment:
import random

from lib.common.session.http.protobuf import ProtoBuf
from lib.common.utils.globals import HTTPJSON_OUT
from lib.common_biz.biz_db_operate import oversea_get_coin_rate
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.replace_parameter import ReplaceParams
from lib.pb_src.python_standard import Recharge_pb2


class Recharge:
    def __init__(self, pay_amount, originalAmount, country, currency, pay_type, version, partner_id):
        self.version = version
        self.partner_id = partner_id
        self.country = country
        # 元 当地币价格
        self.pay_amount = str(pay_amount)
        self.originalAmount = str(originalAmount)
        self.currency = currency
        self.pay_type = pay_type

    def recharge(self):
        rate = oversea_get_coin_rate(self.currency)
        cocoinRechargeAmount = str(round(float(self.pay_amount)/float(rate), 2)/100)
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
            "partnerId": self.partner_id,
            "country": self.country,
            "payType": "upay_gamecard",
            "channel": "upay_gamecard",
            "payAmount": self.pay_amount,
            "currency": self.currency,
            "cocoinRechargeAmount": cocoinRechargeAmount,
            "businessChannelId": "",
            "bankCode": "",
            "pointCardNo": "",
            "pointCardPassword": "",
            "hasAdditionalFees": False,
            "originalAmount": self.pay_amount
        }
        ReplaceParams(req).replace_standard("expend")
        response = ProtoBuf(Recharge_pb2).runner(HTTPJSON_OUT.prefix + '/plugin/cocoin/recharge', 'RechargeRequest'
                                                 , req)
        result = ProtoBuf(Recharge_pb2).parser('RechargeResponse', response)
        return {"pay_req_id": result.data.payRequestId, "partner_order": req["partnerOrder"]}


if __name__ == '__main__':
    Recharge("10000", "10000").recharge()
