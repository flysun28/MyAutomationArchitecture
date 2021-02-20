#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/20 16:42
# comment:
from lib.common.file_operation.config_operation import Config
from lib.common.session.http.protobuf import ProtoBuf
from lib.common.utils.globals import GlobarVar, HTTPJSON_IN
from lib.common_biz.file_path import do_case_path
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.replace_parameter import ReplaceParams
from lib.pb_src.python_standard import SkipPay_pb2


def skip_pay(payAmount, payType="wxpay", partnerId="72724313", app_version=(Config(do_case_path).read_config("sdk_ver", "version")),
             notifyUrl=str(GlobarVar.URL_PAY_IN)+"/notify/receiver"):
    req = {
        "header": {
            "version": "16.0",
            "token": "no_login",
            "model": "PAAM00",
            "apntype": "1",
            "package": "com.example.pay_demo",
            "r_v": "RvDf0ABC",
            "sign": "",
            "sdkVer": "220",
            "appVerison": app_version,
            "ip": "0.0.0.0",
            "openId": "E28C3DF751C14EFAB2D9893DC83058B6c7ab335d8d6d240bca10fdf35c0be85e",
            "brandType": "OPPO",
            "mobileos": "12",
            "androidVersion": "28"
        },
        "partnerOrder": RandomOrder(30).business_order("GC"),
        "partnerId": partnerId,
        "country": "CN",
        "payType": payType,
        "channel": payType,
        # 元
        "payAmount": payAmount,
        "currency": "CNY",
        "product": {
            "name": "NO_LOGIN_PAY",
            "desc": "话费充值",
            "count": "1",
            "priceLocal": payAmount
        },
        "returnUrl": "finzpay://nearme.atlas.com",
        "notifyUrl": notifyUrl,
        "partnerParams": "",
        "extendParams": "",
        "businessChannelId": "",
        "walletVersion": "0",
        "oppoucVersion": "80407",
        "screenInfo": "FULL"
    }
    ReplaceParams(req).replace_standard(pay_method="no_login")
    response = ProtoBuf(SkipPay_pb2).runner(HTTPJSON_IN.prefix + '/plugin/skippay', 'SkipPayRequest', req)
    result = ProtoBuf(SkipPay_pb2).parser('SkipPayResponse', response)


if __name__ == '__main__':
    skip_pay("0.01")