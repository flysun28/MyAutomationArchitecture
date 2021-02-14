#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/8 18:05
# comment:
from lib.common.file_operation.config_operation import Config
from lib.common.utils.globals import HTTPJSON_IN
from lib.common_biz.file_path import account_path, key_path
from lib.pb_src.python_native import SimplePayPb_pb2
from lib.interface_biz.http.pay_pass import Pass
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import expend_pay_sign_string, simple_pay_sign_string
from lib.common.algorithm.rsa import rsa
from lib.common.session.http.protobuf import ProtoBuf
from lib.common.algorithm.cipher import Cipher
from lib.common.file_operation.config_operation import Config
from lib.common_biz.file_path import key_path, account_path


# pass_ = Pass(partner="2031", sdkVer="20600", amount="1.0", package="com.skymoons.hqg.nearme.gamecenter").pass_recharge_spend()
# r_v = pass_[0]
# t_p = pass_[1]
# 
# partnerorder = RandomOrder(32).random_string()
# 
# 
# # def httpjson_simplepay(sdkver, package, amount, partnercode, version='12'):
# req = {"header": {"version": "12.0",
#                   "t_p": t_p,
#                   "imei": "",
#                   "model": "PDCM00",
#                   "apntype": "1",
#                   "package": "com.netease.my.nearme.gamecenter",
#                   "r_v": r_v,
#                   "ext": "",
#                   "sdkVer": 260,
#                   "country": "CN",
#                   "currency": "CNY",
#                   "openId": "",
#                   "brandType": "OPPO",
#                   "mobileos": "16",
#                   "androidVersion": "29"
#                   },
#        "type": "alipay",
#        "amount": "0.02",
#        "cardno": "",
#        "cardpwd": "",
#        "ext": "",
#        "basepay": {"channelId": "",
#                    "notifyurl": "http://cnzx-game-test.wanyol.com/sdklocal/pay/notifyOrder",
#                    "productName": "demo商品名称：",
#                    "productDesc": "oooooo ",
#                    # 业务线
#                    "partnercode": "2031",
#                    "appversion": "208006",
#                    "currencyName": "可币",
#                    "rate": 1.0,
#                    # 商户订单号
#                    "partnerorder": partnerorder
#                    },
#        "sign": "",
#        "ip": "183.238.170.71",
#        "expendRequest": {"header": {"version": "12.0",
#                                     "t_p": t_p,
#                                     "imei": "",
#                                     "model": "PDCM00",
#                                     "apntype": "1",
#                                     "package": "com.netease.my.nearme.gamecenter",
#                                     "r_v": r_v,
#                                     "ext": "",
#                                     "sdkVer": 260,
#                                     "country": "CN",
#                                     "currency": "CNY",
#                                     "openId": "",
#                                     "brandType": "OPPO",
#                                     "mobileos": "16",
#                                     "androidVersion": "29"
#                                     },
#                          "price": 1,
#                          "count": 1,
#                          "productname": "demo商品名称：",
#                          "productdesc": "oooooo ",
#                          "partnerid": "2031",
#                          "callBackUrl": "http://cnzx-game-test.wanyol.com/sdklocal/pay/notifyOrder",
#                          # 商户订单号 与上面一致
#                          "partnerOrder": partnerorder,
#                          "channelId": "",
#                          "ver": "208006",
#                          "source": "梦幻西游",
#                          "attach": "",
#                          # 要算
#                          "sign": "",
#                          "appKey": "bd2sfG91KpSgsSw4Oooo8KcoW",
#                          "voucherId": 1013,
#                          "voucherType": 8,
#                          "voucherCount": 1,
#                          "useVirCoupon": "Y"
#                          },
#        "isNeedExpend": "1",
#        "appId": "",
#        "payTypeRMBType": "0",
#        "tradeType": "common",
#        "screenInfo": "FULL",
#        "buyPlaceId": "10001",
#        "chooseBuyPlace": "Y",
#        "attachGoodsAmount": "2"
# }
# 
# token = 'TOKEN_eyJhbGciOiJFQ0RTQSIsInYiOiIxIn0.eyJleHAiOjE2MTIyNzMxNTE5NDAsImlkIjoiMjA4NjEwMDkwMCIsImlkYyI6InNob3VtaW5nIiwidGlkIjoiemZCcGxpQVV2VEZhWEpOb2ZCL05jMDVKTG45Z3lLK2RPTVh6RnJVZys1ekdNNGdCQ0JzMlpBVmxldE0yUmd2K1E0bXNxNklGd3VNa1I2M3ppbUhWTER1RkFQVVcrNXVaRkRKM1BnS1lDMzQ9In0.MEUCIQCVs6zL5ye3y7AD5yolOXLqQuPo65H6c-yf4yEWgpP4JQIgVFM352Jbog6vlCj3x3ukmSKUJjMT27qbx6msqVyLjKw'
# 
# string_expend_pay = expend_pay_sign_string(
#     token, req['header']['package'],
#     req['expendRequest']['partnerid'],
#     req['expendRequest']['partnerOrder'],
#     req['expendRequest']['productname'],
#     req['expendRequest']['productdesc'],
#     req['expendRequest']['price'],
#     req['expendRequest']['count'])
# print(string_expend_pay)
# string_ = simple_pay_sign_string(req['header']['package'], req['basepay']['partnercode'],
#                                  req['basepay']['partnerorder'], req['amount'], req['type'])
# req['sign'] = Cipher(string_).cipher()
# req['expendRequest']['sign'] = rsa(string_expend_pay, "MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAIxWEg3nFA9F2ajV+abQcE6VGTZecmy4qA4GLpvUgUBRa1E6mbqVGfDjkzzdr9eIcRm/kU6n6uywaWDBxZ4u57EjqQIXmEVPqCwRjL1dF+lIE5QDZTBxqM9GwygQpGYQib42mbCcYB55krZjtfCveKYd0snzpWAnnMx52p3gh9dZAgMBAAECgYAYGB75bBcxmBiKuFIopdjiZQ7zGrwiloGkBsOx1YZreI8oXxtNwZO2nBwHczhhlPd2KEHWc1YOVSuChUJcqkj1C6tionQdOcU02wWXEkxTuGJIArw6ntqYn2ZZZMLBejjRETJZfH/YEPkzUd0FuD0cIfrJUIZOyH3qOWJlEafqQQJBAMkRcGOP4TO/aOasOszDLZe2b15tLjKQe363hV34IgUi4hWQLSdvFG76gpcloi5JXU8IpXeF1q8/bTa4U7RDYw0CQQCyrRXNXGWc/dDnehShi3kOayYrGzKAIvykquDIyLMkAyIobAMSzoj56V+A1sE8C/cyMVwDo8jWcvhCZE3nK+J9AkBd/QvnTnt8AA6ePYYi712hnIMExc6hjk5cFpd+LJ5ifkLmx4WD+HW5xtpCozHjpyG57xXCAEsxklmQCav/CL0FAkApYsYGBzzSHEhjFXfp4zBrEo6ItYgA/hme2qWuXC6CTOeAjWQ42vYHTPL+GMAxdGQRkDVL8of2hDLUzf7taNDRAkBLT1q2MLR1WSJg/EqzJ1enOvxp4L+Pma91IYi0Yr2rA0R06elC3Eut+IMjH3I8ck49TaVbSSClTou11CkSJCyJ")
# response = ProtoBuf(SimplePayPb_pb2).runner(HTTPJSON_IN.prefix+'/plugin/post/simplepay', 'Request', req, flag=0)
# result = ProtoBuf(SimplePayPb_pb2).parser('Result', response)


class SimplePay:

    def __init__(self, chanel, amount, partner_code="2031", sdk_ver=260, version="12.0", version_exp="12.0",
                 notify_url="http://secure.pay-test3.wanyol.com/notify/receiver"):
        """
        :param version:
        :param version_exp:
        :param chanel:
        :param amount: 单位：元
        :param partner_code:
        :param notify_url:
        """
        self.version = version
        self.version_exp = version_exp
        self.chanel = chanel
        self.amount = amount
        self.partner_code = partner_code
        self.notify_url = notify_url
        self.sdk_ver = sdk_ver

    def recharge(self):
        """
        可币充值
        :return:
        """
        tp_rv = Pass().pass_recharge()
        r_v = tp_rv[0]
        t_p = tp_rv[1]
        req = {"header": {"version": self.version, "t_p": t_p, "imei": "", "model": "PCRM00",
                          "apntype": "1", "package": "com.example.pay_demo", "r_v": r_v, "ext": "",
                          "sdkVer": self.sdk_ver, "country": "CN", "currency": "CNY", "openId": "", "brandType": "OPPO",
                          "mobileos": "17", "androidVersion": "29"},
               "type": self.chanel, "amount": self.amount, "cardno": "", "cardpwd": "", "ext": "",
               "basepay": {"channelId": "", "notifyurl": self.notify_url,
                           "productName": "KB—RECHARGE_PAY", "productDesc": "KB—RECHARGE_PAY",
                           "partnercode": self.partner_code,
                           "appversion": "1.1.0", "currencyName": "可币", "rate": 1.0, "partnerorder": "null"},
               "sign": "", "ip": "58.252.5.75", "isNeedExpend": "0", "appId": "", "payTypeRMBType": "0",
               "tradeType": "common", "screenInfo": "FULL"}
        sign_string = simple_pay_sign_string(req['header']['package'], req['basepay']['partnercode'],
                                             req['basepay']['partnerorder'], req['amount'], req['type'])
        req['sign'] = Cipher(sign_string).cipher()
        response = ProtoBuf(SimplePayPb_pb2).runner(HTTPJSON_IN.prefix + '/plugin/post/simplepay', 'Request', req,
                                                    flag=0)
        result = ProtoBuf(SimplePayPb_pb2).parser('Result', response)
        return result

    def direct_pay(self):
        """
        直扣
        :return:
        """
        tp_rv = Pass().pass_direct_pay()
        r_v = tp_rv[0]
        t_p = tp_rv[1]
        req = {"header": {"version": self.version, "t_p": t_p, "imei": "", "model": "PCRM00", "apntype": "1",
                          "package": "com.example.pay_demo", "r_v": r_v, "ext": "", "sdkVer": self.sdk_ver,
                          "country": "CN", "currency": "CNY", "openId": "", "brandType": "OPPO", "mobileos": "17",
                          "androidVersion": "29"},
               "type": self.chanel, "amount": self.amount, "cardno": "", "cardpwd": "", "ext": "",
               "basepay": {"channelId": "", "notifyurl": self.notify_url, "productName": "DIRECT_PAY",
                           "productDesc": "DIRECT_PAY", "partnercode": self.partner_code, "appversion": "1.1.0",
                           "currencyName": "人民币", "rate": 1.0, "partnerorder": RandomOrder(32).random_string()},
               "sign": "", "ip": "58.252.5.75", "isNeedExpend": "0", "appId": "", "payTypeRMBType": "0",
               "tradeType": "common", "screenInfo": "FULL"}
        sign_string = simple_pay_sign_string(req['header']['package'], req['basepay']['partnercode'],
                                             req['basepay']['partnerorder'], req['amount'], req['type'])
        req['sign'] = Cipher(sign_string).cipher()
        response = ProtoBuf(SimplePayPb_pb2).runner(HTTPJSON_IN.prefix + '/plugin/post/simplepay', 'Request', req,
                                                    flag=0)
        result = ProtoBuf(SimplePayPb_pb2).parser('Result', response)
        return result

    def recharge_spend_amount_is_price(self, price):
        """
        充值并消费，渠道支付金额=商品金额，即非点卡情况下，不使用可币与可币券
        :return:
        """
        tp_rv = Pass().pass_recharge_spend()
        r_v = tp_rv[0]
        t_p = tp_rv[1]
        key = Config(key_path).read_config("expend_pay", "key_2031")
        token = Config(account_path).read_config("account", "token")
        partner_order = RandomOrder(32).random_string()
        req = {"header": {"version": self.version, "t_p": t_p, "imei": "", "model": "PDCM00", "apntype": "1",
                          "package": "com.example.pay_demo", "r_v": r_v, "ext": "", "sdkVer": self.sdk_ver,
                          "country": "CN", "currency": "CNY", "openId": "", "brandType": "OPPO", "mobileos": "16",
                          "androidVersion": "29"},
               "type": self.chanel, "amount": self.amount, "cardno": "", "cardpwd": "", "ext": "",
               "basepay": {"channelId": "", "notifyurl": self.notify_url, "productName": "demo", "productDesc": "demo ",
                           "partnercode": self.partner_code, "appversion": "208006", "currencyName": "CNY", "rate": 1.0,
                           "partnerorder": partner_order},
               "sign": "", "ip": "183.238.170.71",
               "expendRequest": {"header": {"version": self.version_exp, "t_p": t_p, "imei": "", "model": "PDCM00",
                                            "apntype": "1", "package": "com.example.pay_demo", "r_v": r_v, "ext": "",
                                            "sdkVer": self.sdk_ver, "country": "CN", "currency": "CNY", "openId": "",
                                            "brandType": "OPPO", "mobileos": "16", "androidVersion": "29"},
                                 "price": price, "count": 1, "productname": "RECHARGE_SPEND_PRICE=AMOUNT",
                                 "productdesc": "RECHARGE_SPEND_PRICE=AMOUNT", "partnerid": self.partner_code,
                                 "callBackUrl": self.notify_url, "partnerOrder": partner_order, "channelId": "",
                                 "ver": "208006", "source": "demo", "attach": "", "sign": "", "factor": ""},
               "isNeedExpend": "1", "appId": "", "payTypeRMBType": "0", "tradeType": "common", "screenInfo": "FULL"}
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
        return result

    def recharge_spend_kb_and_voucher(self, price, vou_id, vou_type, vou_count, factor=""):
        """
        充值并消费，带优惠券，可币金额提现不出来。若账户有可币余额，会扣除。
        :param price: int 单位：分
        :param vou_id: int
        :param vou_type: int
        :param vou_count: int
        :param factor: 优惠券影响因子，用于主题定向优惠券
        :return:
        """
        tp_rv = Pass().pass_recharge_spend()
        r_v = tp_rv[0]
        t_p = tp_rv[1]
        key = Config(key_path).read_config("expend_pay", "key_2031")
        token = Config(account_path).read_config("account", "token")
        partner_order = RandomOrder(32).random_string()
        req = {"header": {"version": self.version, "t_p": t_p, "imei": "", "model": "PDCM00", "apntype": "1",
                          "package": "com.example.pay_demo", "r_v": r_v, "ext": "", "sdkVer": self.sdk_ver,
                          "country": "CN", "currency": "CNY", "openId": "", "brandType": "OPPO", "mobileos": "16",
                          "androidVersion": "29"},
               "type": self.chanel, "amount": self.amount, "cardno": "", "cardpwd": "", "ext": "",
               "basepay": {"channelId": "", "notifyurl": self.notify_url, "productName": "demo", "productDesc": "demo ",
                           "partnercode": self.partner_code, "appversion": "208006", "currencyName": "CNY", "rate": 1.0,
                           "partnerorder": partner_order},
               "sign": "", "ip": "183.238.170.71",
               "expendRequest": {"header": {"version": self.version_exp, "t_p": t_p, "imei": "", "model": "PDCM00",
                                            "apntype": "1", "package": "com.example.pay_demo", "r_v": r_v, "ext": "",
                                            "sdkVer": self.sdk_ver, "country": "CN", "currency": "CNY", "openId": "",
                                            "brandType": "OPPO", "mobileos": "16", "androidVersion": "29"},
                                 "price": price, "count": 1, "productname": "demo", "productdesc": "demo ",
                                 "partnerid": self.partner_code, "callBackUrl": self.notify_url,
                                 "partnerOrder": partner_order, "channelId": "demo", "ver": "208006", "source": "demo",
                                 "attach": "", "sign": "", "appKey": "1234", "voucherId": vou_id,
                                 "voucherType": vou_type, "voucherCount": vou_count, "factor": factor},
               "isNeedExpend": "1", "appId": "", "payTypeRMBType": "0", "tradeType": "common", "screenInfo": "FULL"}
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
        return result

    def recharge_spend_kb_buy_place(self, price, by_id="10001", add_amount="1"):
        """
        有加购位，但不使用优惠券
        注意：amount为实际支付金额，即原商品+加购商品
        :return:
        """
        tp_rv = Pass().pass_recharge_spend()
        r_v = tp_rv[0]
        t_p = tp_rv[1]
        key = Config(key_path).read_config("expend_pay", "key_2031")
        token = Config(account_path).read_config("account", "token")
        partner_order = RandomOrder(32).random_string()
        req = {"header": {"version": self.version, "t_p": t_p, "imei": "", "model": "PDCM00", "apntype": "1",
                          "package": "com.example.pay_demo", "r_v": r_v, "ext": "", "sdkVer": self.sdk_ver,
                          "country": "CN", "currency": "CNY", "openId": "", "brandType": "OPPO", "mobileos": "16",
                          "androidVersion": "29"},
               "type": self.chanel, "amount": self.amount, "cardno": "", "cardpwd": "", "ext": "",
               "basepay": {"channelId": "", "notifyurl": self.notify_url, "productName": "demo", "productDesc": "demo ",
                           "partnercode": self.partner_code, "appversion": "208006", "currencyName": "CNY", "rate": 1.0,
                           "partnerorder": partner_order},
               "sign": "", "ip": "183.238.170.71",
               "expendRequest": {"header": {"version": self.version_exp, "t_p": t_p, "imei": "", "model": "PDCM00",
                                            "apntype": "1", "package": "com.example.pay_demo", "r_v": r_v, "ext": "",
                                            "sdkVer": self.sdk_ver, "country": "CN", "currency": "CNY", "openId": "",
                                            "brandType": "OPPO", "mobileos": "16", "androidVersion": "29"},
                                 "price": price, "count": 1, "productname": "RECHARGE_SPEND_PRICE=AMOUNT",
                                 "productdesc": "RECHARGE_SPEND_PRICE=AMOUNT", "partnerid": self.partner_code,
                                 "callBackUrl": self.notify_url, "partnerOrder": partner_order, "channelId": "",
                                 "ver": "208006", "source": "demo", "attach": "", "sign": "", "factor": ""},
               "isNeedExpend": "1", "appId": "", "payTypeRMBType": "0", "tradeType": "common", "screenInfo": "FULL",
               "buyPlaceId": by_id, "chooseBuyPlace": "Y", "attachGoodsAmount": add_amount}
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
        return result

    def recharge_spend_kb_voucher_buy_place(self, price, vou_id, vou_count, by_id, add_amount, vou_type=8):
        """
        加购位，使用红包券
        加购位优惠券信息：`pay_baseshop`.`virtual_voucher_info`
        :return:
        """
        tp_rv = Pass().pass_recharge_spend()
        r_v = tp_rv[0]
        t_p = tp_rv[1]
        key = Config(key_path).read_config("expend_pay", "key_2031")
        token = Config(account_path).read_config("account", "token")
        partner_order = RandomOrder(32).random_string()
        req = {"header": {"version": self.version, "t_p": t_p, "imei": "", "model": "PDCM00", "apntype": "1",
                          "package": "com.example.pay_demo", "r_v": r_v, "ext": "", "sdkVer": self.sdk_ver,
                          "country": "CN", "currency": "CNY", "openId": "", "brandType": "OPPO", "mobileos": "16",
                          "androidVersion": "29"},
               "type": self.chanel, "amount": self.amount, "cardno": "", "cardpwd": "", "ext": "",
               "basepay": {"channelId": "", "notifyurl": self.notify_url, "productName": "demo", "productDesc": "demo ",
                           "partnercode": self.partner_code, "appversion": "208006", "currencyName": "CNY", "rate": 1.0,
                           "partnerorder": partner_order},
               "sign": "", "ip": "183.238.170.71",
               "expendRequest": {"header": {"version": self.version_exp, "t_p": t_p, "imei": "", "model": "PDCM00",
                                            "apntype": "1", "package": "com.example.pay_demo", "r_v": r_v, "ext": "",
                                            "sdkVer": self.sdk_ver, "country": "CN", "currency": "CNY", "openId": "",
                                            "brandType": "OPPO", "mobileos": "16", "androidVersion": "29"},
                                 "price": price, "count": 1, "productname": "demo", "productdesc": "demo ",
                                 "partnerid": self.partner_code, "callBackUrl": self.notify_url,
                                 "partnerOrder": partner_order, "channelId": "demo", "ver": "208006", "source": "demo",
                                 "attach": "", "sign": "", "appKey": "1234", "voucherId": vou_id,
                                 "voucherType": vou_type, "voucherCount": vou_count, "factor": "",
                                 "useVirCoupon": "Y"},
               "isNeedExpend": "1", "appId": "", "payTypeRMBType": "0", "tradeType": "common", "screenInfo": "FULL",
               "buyPlaceId": by_id, "chooseBuyPlace": "Y", "attachGoodsAmount": add_amount}
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
        return result


def http_pb_simplepay(req:dict):
#     token = 'TOKEN_eyJhbGciOiJFQ0RTQSIsInYiOiIxIn0.eyJleHAiOjE2MTIyNzMxNTE5NDAsImlkIjoiMjA4NjEwMDkwMCIsImlkYyI6InNob3VtaW5nIiwidGlkIjoiemZCcGxpQVV2VEZhWEpOb2ZCL05jMDVKTG45Z3lLK2RPTVh6RnJVZys1ekdNNGdCQ0JzMlpBVmxldE0yUmd2K1E0bXNxNklGd3VNa1I2M3ppbUhWTER1RkFQVVcrNXVaRkRKM1BnS1lDMzQ9In0.MEUCIQCVs6zL5ye3y7AD5yolOXLqQuPo65H6c-yf4yEWgpP4JQIgVFM352Jbog6vlCj3x3ukmSKUJjMT27qbx6msqVyLjKw'
    token = Config(account_path).read_config("account", "token")
    string_expend_pay = expend_pay_sign_string(
        token, req['header']['package'],
        req['expendRequest']['partnerid'],
        req['expendRequest']['partnerOrder'],
        req['expendRequest']['productname'],
        req['expendRequest']['productdesc'],
        req['expendRequest']['price'],
        req['expendRequest']['count'])
    string_ = simple_pay_sign_string(req['header']['package'], req['basepay']['partnercode'],
                                     req['basepay']['partnerorder'], req['amount'], req['type'])
    req['sign'] = Cipher(string_).cipher()
    req['expendRequest']['sign'] = rsa(string_expend_pay, "MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAIxWEg3nFA9F2ajV+abQcE6VGTZecmy4qA4GLpvUgUBRa1E6mbqVGfDjkzzdr9eIcRm/kU6n6uywaWDBxZ4u57EjqQIXmEVPqCwRjL1dF+lIE5QDZTBxqM9GwygQpGYQib42mbCcYB55krZjtfCveKYd0snzpWAnnMx52p3gh9dZAgMBAAECgYAYGB75bBcxmBiKuFIopdjiZQ7zGrwiloGkBsOx1YZreI8oXxtNwZO2nBwHczhhlPd2KEHWc1YOVSuChUJcqkj1C6tionQdOcU02wWXEkxTuGJIArw6ntqYn2ZZZMLBejjRETJZfH/YEPkzUd0FuD0cIfrJUIZOyH3qOWJlEafqQQJBAMkRcGOP4TO/aOasOszDLZe2b15tLjKQe363hV34IgUi4hWQLSdvFG76gpcloi5JXU8IpXeF1q8/bTa4U7RDYw0CQQCyrRXNXGWc/dDnehShi3kOayYrGzKAIvykquDIyLMkAyIobAMSzoj56V+A1sE8C/cyMVwDo8jWcvhCZE3nK+J9AkBd/QvnTnt8AA6ePYYi712hnIMExc6hjk5cFpd+LJ5ifkLmx4WD+HW5xtpCozHjpyG57xXCAEsxklmQCav/CL0FAkApYsYGBzzSHEhjFXfp4zBrEo6ItYgA/hme2qWuXC6CTOeAjWQ42vYHTPL+GMAxdGQRkDVL8of2hDLUzf7taNDRAkBLT1q2MLR1WSJg/EqzJ1enOvxp4L+Pma91IYi0Yr2rA0R06elC3Eut+IMjH3I8ck49TaVbSSClTou11CkSJCyJ")
    response = ProtoBuf(SimplePayPb_pb2).runner(HTTPJSON_IN.prefix+'/plugin/post/simplepay', 'Request', req, flag=0)
    result = ProtoBuf(SimplePayPb_pb2).parser('Result', response)
    return result


if __name__ == '__main__':
    #SimplePay("wxpay", "1").recharge_spend_amount_is_price(1)
    #SimplePay("wxpay", "10").recharge_spend_kb_and_voucher(1, 10001, 2, 22)
    SimplePay("wxpay", "10").recharge_spend_kb_buy_place(1)
