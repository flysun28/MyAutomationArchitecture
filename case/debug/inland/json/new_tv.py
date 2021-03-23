#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/8 16:40
# comment:
from lib.common.algorithm.sha_256 import sha_256
from lib.common.utils.globals import GlobalVar
from lib.common_biz.find_key import GetKey, is_get_key_from_db
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign


class NewTv:
    def __init__(self):
        pass

    def pay_order(self):
        case_data = {
            'version': '1.0.0',
            'partnerCode': '72727676',
            'partnerOrder': RandomOrder(30).business_order("TV"),
            'countryCode': 'CN',
            'currency': 'CNY',
            'payType': 'newtv',
            # 'payType': 'wxpay',
            'channel': 'newtv-qrcode',
            'payAmount': '1',
            'requestTime': '202006101810',
            'productName': 'test',
            'productDesc': 'TEST',
            'count': '1',
            'notifyUrl': 'www.baidu.com',
            'attach': '1',
            'extendParams': '',
            'sign': ''
        }
        temp_string = ''
        if is_get_key_from_db():
            temp_string = Sign(case_data).join_asc_have_key("&key=") + GetKey(case_data['partnerCode']).get_key_from_merchant()
        else:
            temp_string = Sign(case_data).join_asc_have_key("&key=") + "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCJOiGsoifR0qAwpb72gbbDonYgJ973LBOzSa+SGccbl9Hyv/7Rnkoet015dieP5lTHbQiUcWrX3DVhLUM+9q8loTYETVvBjYi+fDtOIbUUdmaObCKmdHl1SSZlMHVGkbQ8yys8bqkw0DbBQuqN6WdYexcyFfrh1EvDol0c9o1l/wIDAQAB"
        case_data['sign'] = sha_256(temp_string)
        """
        http://gw-opay.oppomobile.com/gateway/payOrder
        MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCJOiGsoifR0qAwpb72gbbDonYgJ973LBOzSa+SGccbl9Hyv/7Rnkoet015dieP5lTHbQiUcWrX3DVhLUM+9q8loTYETVvBjYi+fDtOIbUUdmaObCKmdHl1SSZlMHVGkbQ8yys8bqkw0DbBQuqN6WdYexcyFfrh1EvDol0c9o1l/wIDAQAB
        """
        GlobalVar.HTTPJSON_GW_IN.post("/gateway/payOrder", data=case_data)

    def sign_order(self):
        case_data = {
            'partnerOrder': RandomOrder(30).business_order("TV"),
            'partnerId': '72727676',
            # 'payType': 'wxpay',
            'payType': 'newtv',
            'orderName': '1个月',
            'userId': '2000001',
            'productId': '666666885',
            'countryCode': 'CN',
            'currency': 'CNY',
            'amount': 1,
            'nextAmount': 1,
            'notifyUrl': 'http://account-television-test.wanyol.com/v1/account/order/payment/notify/mgtv',
            'returnUrl': 'https://opaycenter-gw.nearme.com.cn/opaycenter/newtvAutoRenewSignNotify',
            'ip': '210.22.6.84',
            'planId': '122222',
            'interval': 1,
            'intervalType': 1,
            'contractNotifyUrl': 'http://account-television-test.wanyol.com/v1/account/order/sign/notify/mgtv',
            'papayType': 2,
            'aheadOfTime': 86300,
            'sign': ''
        }
        temp_string = Sign(case_data).join_asc_have_key("&key=") + GetKey(
            case_data['partnerId']).get_key_from_merchant()
        case_data['sign'] = sha_256(temp_string)
        GlobalVar.HTTPJSON_GW_IN.post("/gateway/wxpay/qrcode/signAndPay", data=case_data)

    def query_order(self):
        pass

    def query_sign(self):
        pass


if __name__ == '__main__':
    NewTv().pay_order()
