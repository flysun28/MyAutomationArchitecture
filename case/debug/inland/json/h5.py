#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/8 15:23
# comment:
import random
from lib.common.algorithm.sha_256 import sha_256
from lib.common.utils.globals import GlobarVar
from lib.common_biz.find_key import GetKey
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign
order = RandomOrder(32).business_order("H")


class H5:
    def __init__(self):
        pass

    def qr_code_trade(self):
        case_dict = {
            "accessType": "NATIVE",
            "serviceType": "PAY",
            # SIGNANDPAY PAY
            "userInfo": {
                "ssoid": str(2100000000 + random.randint(100, 1000000))
            },
            "partnerCode": "72724324",
            # SIGNANDPAY 需要带上该信息
            "contractInfo": {
                "contractPartnerOrder": RandomOrder(32).random_num(),
                "contractNotifyUrl": "http://pay.pay-test.wanyol.com/notify/receiver",
                "renewProductCode": "727243140027"
                # "renewProductCode": "727243240001"
            },
            "sign": "",
            "attach": "attachtest",
            "returnUrl": "https://i-insurance-test.wanyol.com/insurance/product/details/resultCommon/?orderNo=" + order
                         ,
            "payInfo": {
                "country": "CN",
                "amount": 1,
                "partnerOrder": order,
                "notifyUrl": "http://pay.pay-test.wanyol.com/notify/receiver",
                "currency": "CNY"
            },
            "goodsInfo": {
                "subject": "H5-TEST"
            }
        }
        temp_string = Sign(case_dict).join_asc_have_key("&key=") + GetKey(case_dict['partnerCode']).get_key_from_merchant()
        temp_string = temp_string.replace("'", '"')
        temp_string = temp_string.replace(" ", '')
        case_dict['sign'] = sha_256(temp_string)
        GlobarVar.HTTPJSON_GW_IN.post("/pay/qrCode/trade", data=case_dict)


if __name__ == '__main__':
    H5().qr_code_trade()