#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/8 17:52
# comment:
from lib.common.algorithm.md5 import md5
from lib.common.utils.globals import GlobarVar
from lib.common_biz.find_key import GetKey
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign


class AutoRenew:
    def __init__(self):
        pass

    def auto_renew_out(self):
        """
        像渠道发起扣费接口
        :return:
        """
        case_dict = {
            'agreementNo': '202101145806346066',
            'ssoid': '2076075925',
            'renewProductCode': '20310001',
            'partnerCode': '2031',
            'partnerOrder': RandomOrder(32).random_num(),
            'payType': 'wxpay',
            'amount': '0.01',
            'currencyName': 'CNY',
            'country': 'CN',
            'subject': '测试商品',
            'desc': 'Default product desc...',
            'notifyUrl': 'http://pay.pay-test.wanyol.com/notify/notify/receiver',
            'apppackage': 'com.example.pay_demo',
            'thirdPartId': 'oCg6Xt5tTdorouaXfGcjtYKHgT0Y',
            'imei': '',
            'model': '',
            'ip': '',
            'ext': '',
            # 签名未校验
            'sign': '54e272460778bb54ea470c7a3ad60531'
        }
        temp_string = Sign(case_dict).join_asc_have_key() + GetKey(case_dict['partnerCode']).get_key_from_merchant()
        case_dict['sign'] = md5(temp_string)
        GlobarVar.HTTPJSON_IN.post("/plugin/autorenew/autorenewpay", data=case_dict)

    def query_sign(self):
        """
        签约查询
        :return:
        """
        case_dict = {
            "ssoid": "2000071235",
            "renewProductCode": "727243140011",
            "partnerCode": "72724314",
            "currencyName": "CNY",
            "country": "CN",
            "sign": "efe9a9b2d3b058789cdd51ed007e5860"
        }
        GlobarVar.HTTPJSON_IN.post("/plugin/autorenew/querysign", data=case_dict)

    def un_sign(self):
        """
        解约。微信需手动，因签约回调去了生产。支付宝仅可在第一套环境，回调地址在支付宝配置死了。
        :return:
        """
        case_dict = {
            'agreementNo': '20206016688077832660',
            'ssoid': '2076082038',
            'renewProductCode': '20310001',
            'partnerCode': '2031',
            'partnerOrder': RandomOrder(32).business_order(""),
            'payType': 'alipay',
            'currencyName': 'CNY',
            'country': 'CN',
            'sign': ''
        }
        temp_string = Sign(case_dict).join_asc_have_key() + GetKey(case_dict['partnerCode']).get_key_from_merchant()
        case_dict['sign'] = md5(temp_string)
        GlobarVar.HTTPJSON_IN.post("/plugin/autorenew/unsign", data=case_dict)


if __name__ == '__main__':
    AutoRenew().un_sign()