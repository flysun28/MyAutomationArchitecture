#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/8 18:05
# comment:
from lib.common.file_operation.config_operation import Config
from lib.common.utils.globals import HTTPJSON_IN, GlobarVar
from lib.common_biz.file_path import account_path, key_path
from lib.pb_src.python_native import SimplePayPb_pb2
from lib.interface_biz.http.pay_pass import Pass
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import expend_pay_sign_string, simple_pay_sign_string
from lib.common.algorithm.rsa import rsa
from lib.common.session.http.protobuf import ProtoBuf
from lib.common.algorithm.cipher import Cipher


class SimplePay:

    def __init__(self):
        pass

    def recharge(self):
        tp_rv = Pass().pass_recharge()
        r_v = tp_rv[0]
        t_p = tp_rv[1]
        req = {"header": {"version": "12.0", "t_p": t_p, "imei": "", "model": "PCRM00",
                          "apntype": "1", "package": "com.example.pay_demo", "r_v": r_v, "ext": "", "sdkVer": 260,
                          "country": "CN", "currency": "CNY", "openId": "", "brandType": "OPPO", "mobileos": "17",
                          "androidVersion": "29"},
               "type": "alipay", "amount": "20.0", "cardno": "", "cardpwd": "", "ext": "",
               "basepay": {"channelId": "", "notifyurl": "http://secure.pay-test3.wanyol.com/notify/receiver",
                           "productName": "KB—RECHARGE", "productDesc": "RECHARGE",
                           "partnercode": "2031",
                           "appversion": "1.1.0", "currencyName": "可币", "rate": 1.0, "partnerorder": "null"},
               "sign": "", "ip": "58.252.5.75", "isNeedExpend": "0", "appId": "", "payTypeRMBType": "0",
               "tradeType": "common", "screenInfo": "FULL"}
        sign_string = simple_pay_sign_string(req['header']['package'], req['basepay']['partnercode'],
                                             req['basepay']['partnerorder'], req['amount'], req['type'])
        req['sign'] = Cipher(sign_string).cipher()
        response = ProtoBuf(SimplePayPb_pb2).runner(HTTPJSON_IN.prefix + '/plugin/post/simplepay', 'Request', req,
                                                    flag=0)
        result = ProtoBuf(SimplePayPb_pb2).parser('Result', response)

    def direct_pay(self):
        tp_rv = Pass().pass_direct_pay()
        r_v = tp_rv[0]
        t_p = tp_rv[1]
        req = {"header": {"version": "12.0", "t_p": t_p, "imei": "", "model": "PCRM00", "apntype": "1",
                          "package": "com.example.pay_demo", "r_v": r_v, "ext": "", "sdkVer": 260,
                          "country": "CN", "currency": "CNY","openId": "", "brandType": "OPPO", "mobileos": "17",
                          "androidVersion": "29"},
               "type": "alipay", "amount": "100.0", "cardno": "", "cardpwd": "", "ext": "",
               "basepay": {"channelId": "", "notifyurl": "http://secure.pay-test3.wanyol.com/notify/receiver",
                           "productName": "直扣","productDesc": "直扣", "partnercode": "2031", "appversion": "1.1.0",
                           "currencyName": "人民币", "rate": 1.0, "partnerorder": RandomOrder(32).random_string()},
               "sign": "", "ip": "58.252.5.75", "isNeedExpend": "0", "appId": "","payTypeRMBType": "0",
               "tradeType": "common", "screenInfo": "FULL"}
        sign_string = simple_pay_sign_string(req['header']['package'], req['basepay']['partnercode'],
                                             req['basepay']['partnerorder'], req['amount'], req['type'])
        req['sign'] = Cipher(sign_string).cipher()
        response = ProtoBuf(SimplePayPb_pb2).runner(HTTPJSON_IN.prefix + '/plugin/post/simplepay', 'Request', req,
                                                    flag=0)
        result = ProtoBuf(SimplePayPb_pb2).parser('Result', response)

    def recharge_spend_ke_and_voucher(self):
        tp_rv = Pass().pass_recharge_spend()
        r_v = tp_rv[0]
        t_p = tp_rv[1]
        key = Config(key_path).read_config("expend_pay", "key_2031")
        token = Config(account_path).read_config("account", "token")
        partner_order = RandomOrder(32).random_string()
        req = {"header": {"version": "12.0", "t_p": t_p, "imei": "", "model": "PDCM00", "apntype": "1",
                          "package": "com.example.pay_demo", "r_v": r_v, "ext": "", "sdkVer": 260, "country": "CN",
                          "currency": "CNY", "openId": "", "brandType": "OPPO", "mobileos": "16",
                          "androidVersion": "29"},
               "type": "alipay", "amount": "10.02", "cardno": "", "cardpwd": "", "ext": "",
               "basepay": {"channelId": "", "notifyurl": "http://cnzx-game-test.wanyol.com/sdklocal/pay/notifyOrder",
                           "productName": "demo", "productDesc": "demo ", "partnercode": "2031", "appversion": "208006",
                           "currencyName": "CNY", "rate": 1.0, "partnerorder": partner_order},
               "sign": "", "ip": "183.238.170.71",
               "expendRequest": {
                   "header": {"version": "12.0", "t_p": t_p, "imei": "", "model": "PDCM00", "apntype": "1",
                              "package": "com.example.pay_demo", "r_v": r_v, "ext": "", "sdkVer": 260,
                              "country": "CN", "currency": "CNY", "openId": "", "brandType": "OPPO",
                              "mobileos": "16", "androidVersion": "29"},
                   "price": 30000, "count": 1, "productname": "demo", "productdesc": "demo ", "partnerid": "2031",
                   "callBackUrl": "http://pay.pay-test.wanyol.com/notify/notify/receiver",
                   "partnerOrder": partner_order, "channelId": "demo", "ver": "208006", "source": "demo",
                   "attach": "", "sign": "", "appKey": "1234", "voucherId": 101300, "voucherType": 2,
                   "voucherCount": 0, "factor": "sjh", "useVirCoupon": "Y"
                   },
               # isNeedExpend:0, 充值与直扣场景；isNeedExpend:1，充值消费，纯消费
               # "payTypeRMBType": "0"，非MSP；"payTypeRMBType": "1"，MSP？？？
               # "tradeType": "common" 普通支付, "tradeType": "single" 单机
               "isNeedExpend": "0", "appId": "", "payTypeRMBType": "0", "tradeType": "common", "screenInfo": "FULL",
               # 会员加购信息，attachGoodsAmount服务端做了校验
               "buyPlaceId": "10001", "chooseBuyPlace": "Y", "attachGoodsAmount": "1"}
        string_expend_pay = expend_pay_sign_string(token, req['header']['package'], req['expendRequest']['partnerid'],
                                                   req['expendRequest']['partnerOrder'],
                                                   req['expendRequest']['productname'],
                                                   req['expendRequest']['productdesc'], req['expendRequest']['price'],
                                                   req['expendRequest']['count'])
        sign_string = simple_pay_sign_string(req['header']['package'], req['basepay']['partnercode'],
                                             req['basepay']['partnerorder'], req['amount'], req['type'])
        req['sign'] = Cipher(sign_string).cipher()
        req['expendRequest']['sign'] = rsa(string_expend_pay, key)
        response = ProtoBuf(SimplePayPb_pb2).runner(HTTPJSON_IN.prefix + '/plugin/post/simplepay', 'Request', req,
                                                    flag=0)
        result = ProtoBuf(SimplePayPb_pb2).parser('Result', response)



if __name__ == '__main__':
    SimplePay().direct_pay()