#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/8 16:41
# comment:
import time

from lib.common.algorithm.md5 import md5
from lib.common.algorithm.sha_256 import sha_256
from lib.common.utils.globals import GlobarVar
from lib.common_biz.find_key import GetKey
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign


class Msp:
    def __init__(self):
        pass

    def pay_trade(self):
        case_dict = {
            "accessType": "NATIVE",
            # appKey: `platform_opay`.`t_key`
            "appKey": "2031",
            # "contractInfo": str({'contractNotifyUrl': 'http://pay.pay-test.wanyol.com/notify/receiver','contractPartnerOrder': partner_order("SN"),
            #                      'renewProductCode': '20320004'}),
            "goodsInfo": str({'originalAmount': 100, 'subject': 'OPPOSONG1'}),
            "nonce": RandomOrder(32).random_num(),
            "partnerCode": "2032",
            "payInfo": str({'amount': 1, 'country': 'CN', 'currency': 'CNY',
                            'notifyUrl': 'http://pay.pay-test.wanyol.com/notify/receiver',
                            'partnerOrder': RandomOrder(32).random_num()}),
            "returnUrl": "http://www.baidu.com",
            # SIGNANDPAY
            "serviceType": "PAY",
            "timestamp": "1601437709207",
            # platform固定MSP_TV, 区分msp手机端与电视端
            "userInfo": str({'platform': 'MSP_TV', 'ssoid': '2076075925', 'thirdPartId': '111'}),
            "sign": ""
        }
        sign_string = Sign(case_dict).join_asc_have_key("&key=") + GetKey("2031").get_key_from_t_key()
        case_dict['sign'] = md5(sign_string, to_upper=False)
        GlobarVar.HTTPJSON_IN.post("/api/pay/v1/trade", data=case_dict)

    def query_result(self):
        case_dict = {
            "partnerOrder": "zKljSk1yGaVfYcZOAunHUTw7IB9CEerp", "queryType": "PAY"
        }
        GlobarVar.HTTPJSON_IN.post("/api/pay/v1/qrcode/order-query-result", data=case_dict)


class Msp_NewTV:
    def __init__(self):
        pass

    def msp_pay_order(self):
        case_data = {
            'version': '1.0.0',
            'partnerCode': '2031',
            'partnerOrder': RandomOrder(29).business_order("MTV"),
            'countryCode': 'CN',
            'currency': 'CNY',
            'payType': 'newtv',
            # 'payType': 'wxpay',newtv
            'channel': 'newtv-qrcode',
            # channel: alipay-qrcode， wxpay-qrcode
            'payAmount': '1',
            'requestTime': time.strftime('%Y%m%d%H%M%S', time.localtime()),
            'productName': 'MSP-TEST',
            'productDesc': 'MSP-TEST',
            'count': '1',
            'notifyUrl': 'http://pay.pay-test.wanyol.com/notify/receiver',
            'attach': 'SZ_ONE',
            'extendParams': '',
            # MSP本次新增，若是msp来源，传MSP
            'platform': 'MSP',
            'sign': ''
        }
        temp_string = Sign(case_data).join_asc_have_key("&key=") + GetKey(
            case_data['partnerCode']).get_key_from_merchant()
        case_data['sign'] = sha_256(temp_string)
        GlobarVar.HTTPJSON_GW_IN.post("/gateway/payOrder", data=case_data)

    def msp_sign_and_pay(self):
        """
        签约续费只能newtv渠道
        :return:
        """
        case_data = {
            'partnerOrder': RandomOrder(29).business_order("MTV"),
            'partnerId': '2031',
            # 'payType': 'wxpay',
            'payType': 'newtv',
            'orderName': '1个月',
            'userId': '2076075925',
            # 'userId': '2000001',
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
            # MSP本次新增，若是msp来源，传MSP
            'platform': 'MSP',
            'sign': ''
        }
        temp_string = Sign(case_data).join_asc_have_key("&key=") + GetKey(
            case_data['partnerId']).get_key_from_merchant()
        case_data['sign'] = sha_256(temp_string)
        GlobarVar.HTTPJSON_GW_IN.post("/gateway/wxpay/qrcode/signAndPay", data=case_data)

    def msp_query_result(self):
        case_data = {
            # 支付订单号
            "payReqId": "RM202012081733370000123456680642",
            "queryType": "PAY",
            # "queryType": "PAY", SIGNANDPAY,
            # 商户订单号
            "partnerOrder": "TV202012081733307952298093395196"
        }
        GlobarVar.HTTPJSON_IN.post("/api/pay/v1/qrcode/order-query-result", data=case_data)

    def msp_sign_cancel(self):
        case_data = {
            # partnerOrder 对应签约订单传入的商户订单订单号才能解约
            "partnerOrder": 'TV202012081854190886096623142470',
            "payType": "newtv",
            "notifyUrl": "http://pay.pay-test.wanyol.com/notify/receiver",
            "partnerId": "2031",
            "sign": ""
        }
        temp_string = Sign(case_data).join_asc_have_key("&key=") + GetKey(
            case_data['partnerId']).get_key_from_merchant()
        case_data['sign'] = sha_256(temp_string)
        GlobarVar.HTTPJSON_GW_IN.post("/gateway/sign/cancel", data=case_data)


if __name__ == '__main__':
    Msp_NewTV().msp_sign_cancel()
