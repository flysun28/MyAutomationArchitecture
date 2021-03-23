#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/8 16:35
# comment:
from lib.common.algorithm.sha_256 import sha_256
from lib.common.utils.globals import GlobalVar
from lib.common_biz.find_key import GetKey
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign


class Ios:
    def __init__(self):
        pass

    def create_order(self):
        case_dict = {
            "partnerCode": "4692862",
            "payType": "APPSTORE",
            "sign": "",
            "iapUserInfo": {
                "appPackage": "com.oppo.usercenter",
                "ssoId": "ere8r78e",
                "thirdPartId": "4564645",
                "userIp": "10.102.186.23"
            },
            "iapPayInfo": {
                "country": "CN",
                "amount": 1000,
                "partnerOrder":  RandomOrder(30).business_order("OS"),
                "notifyUrl": "http://pay.pay-test.wanyol.com/notify/notify/receiver",
                "currency": "CNY",
            },
            "iapGoodsInfo": {
                "subject": "智能家居iOS内购"
            }
        }
        temp_string = Sign(case_dict).join_asc_have_key("&key=") + GetKey(case_dict['partnerCode']).get_key_from_merchant()
        temp_string = temp_string.replace("'", '"')
        temp_string = temp_string.replace(" ", '')
        case_dict['sign'] = sha_256(temp_string)
        GlobalVar.HTTPJSON_GW_IN.post("/gateway/api/orderCreate", data=case_dict)


if __name__ == '__main__':
    Ios().create_order()