# coding=utf-8

from lib.common.utils.globals import HTTPJSON_IN, GlobarVar
from lib.pb_src.python_native import SimplePayPb_pb2
from lib.interface_biz.http.pay_pass import Pass
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import expend_pay_sign_string, simple_pay_sign_string
from lib.common.algorithm.rsa import rsa
from lib.common.session.http.protobuf import ProtoBuf
from lib.common.algorithm.cipher import Cipher



pass_ = Pass(partner="2031", sdkVer="20600", amount="1.0", package="com.skymoons.hqg.nearme.gamecenter").pass_recharge_spend()
r_v = pass_[0]
t_p = pass_[1]

partnerorder = RandomOrder(32).random_string()


# def httpjson_simplepay(sdkver, package, amount, partnercode, version='12'):
req = {"header": {"version": "12.0",
                  "t_p": t_p,
                  "imei": "",
                  "model": "PDCM00",
                  "apntype": "1",
                  "package": "com.netease.my.nearme.gamecenter",
                  "r_v": r_v,
                  "ext": "",
                  "sdkVer": 260,
                  "country": "CN",
                  "currency": "CNY",
                  "openId": "",
                  "brandType": "OPPO",
                  "mobileos": "16",
                  "androidVersion": "29"
                  },
       "type": "alipay",
       "amount": "0.02",
       "cardno": "",
       "cardpwd": "",
       "ext": "",
       "basepay": {"channelId": "",
                   "notifyurl": "http://cnzx-game-test.wanyol.com/sdklocal/pay/notifyOrder",
                   "productName": "demo商品名称：",
                   "productDesc": "oooooo ",
                   # 业务线
                   "partnercode": "2031",
                   "appversion": "208006",
                   "currencyName": "可币",
                   "rate": 1.0,
                   # 商户订单号
                   "partnerorder": partnerorder
                   },
       "sign": "",
       "ip": "183.238.170.71",
       "expendRequest": {"header": {"version": "12.0",
                                    "t_p": t_p,
                                    "imei": "",
                                    "model": "PDCM00",
                                    "apntype": "1",
                                    "package": "com.netease.my.nearme.gamecenter",
                                    "r_v": r_v,
                                    "ext": "",
                                    "sdkVer": 260,
                                    "country": "CN",
                                    "currency": "CNY",
                                    "openId": "",
                                    "brandType": "OPPO",
                                    "mobileos": "16",
                                    "androidVersion": "29"
                                    },
                         "price": 1,
                         "count": 1,
                         "productname": "demo商品名称：",
                         "productdesc": "oooooo ",
                         "partnerid": "2031",
                         "callBackUrl": "http://cnzx-game-test.wanyol.com/sdklocal/pay/notifyOrder",
                         # 商户订单号 与上面一致
                         "partnerOrder": partnerorder,
                         "channelId": "",
                         "ver": "208006",
                         "source": "梦幻西游",
                         "attach": "",
                         # 要算
                         "sign": "",
                         "appKey": "bd2sfG91KpSgsSw4Oooo8KcoW",
                         "voucherId": 1013,
                         "voucherType": 8,
                         "voucherCount": 1,
                         "useVirCoupon": "Y"
                         },
       "isNeedExpend": "1",
       "appId": "",
       "payTypeRMBType": "0",
       "tradeType": "common",
       "screenInfo": "FULL",
       "buyPlaceId": "10001",
       "chooseBuyPlace": "Y",
       "attachGoodsAmount": "2"
}

token = 'TOKEN_eyJhbGciOiJFQ0RTQSIsInYiOiIxIn0.eyJleHAiOjE2MTIyNzMxNTE5NDAsImlkIjoiMjA4NjEwMDkwMCIsImlkYyI6InNob3VtaW5nIiwidGlkIjoiemZCcGxpQVV2VEZhWEpOb2ZCL05jMDVKTG45Z3lLK2RPTVh6RnJVZys1ekdNNGdCQ0JzMlpBVmxldE0yUmd2K1E0bXNxNklGd3VNa1I2M3ppbUhWTER1RkFQVVcrNXVaRkRKM1BnS1lDMzQ9In0.MEUCIQCVs6zL5ye3y7AD5yolOXLqQuPo65H6c-yf4yEWgpP4JQIgVFM352Jbog6vlCj3x3ukmSKUJjMT27qbx6msqVyLjKw'

string_expend_pay = expend_pay_sign_string(
    token, req['header']['package'],
    req['expendRequest']['partnerid'],
    req['expendRequest']['partnerOrder'],
    req['expendRequest']['productname'],
    req['expendRequest']['productdesc'],
    req['expendRequest']['price'],
    req['expendRequest']['count'])
print(string_expend_pay)
string_ = simple_pay_sign_string(req['header']['package'], req['basepay']['partnercode'],
                                 req['basepay']['partnerorder'], req['amount'], req['type'])
req['sign'] = Cipher(string_).cipher()
req['expendRequest']['sign'] = rsa(string_expend_pay, "MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAIxWEg3nFA9F2ajV+abQcE6VGTZecmy4qA4GLpvUgUBRa1E6mbqVGfDjkzzdr9eIcRm/kU6n6uywaWDBxZ4u57EjqQIXmEVPqCwRjL1dF+lIE5QDZTBxqM9GwygQpGYQib42mbCcYB55krZjtfCveKYd0snzpWAnnMx52p3gh9dZAgMBAAECgYAYGB75bBcxmBiKuFIopdjiZQ7zGrwiloGkBsOx1YZreI8oXxtNwZO2nBwHczhhlPd2KEHWc1YOVSuChUJcqkj1C6tionQdOcU02wWXEkxTuGJIArw6ntqYn2ZZZMLBejjRETJZfH/YEPkzUd0FuD0cIfrJUIZOyH3qOWJlEafqQQJBAMkRcGOP4TO/aOasOszDLZe2b15tLjKQe363hV34IgUi4hWQLSdvFG76gpcloi5JXU8IpXeF1q8/bTa4U7RDYw0CQQCyrRXNXGWc/dDnehShi3kOayYrGzKAIvykquDIyLMkAyIobAMSzoj56V+A1sE8C/cyMVwDo8jWcvhCZE3nK+J9AkBd/QvnTnt8AA6ePYYi712hnIMExc6hjk5cFpd+LJ5ifkLmx4WD+HW5xtpCozHjpyG57xXCAEsxklmQCav/CL0FAkApYsYGBzzSHEhjFXfp4zBrEo6ItYgA/hme2qWuXC6CTOeAjWQ42vYHTPL+GMAxdGQRkDVL8of2hDLUzf7taNDRAkBLT1q2MLR1WSJg/EqzJ1enOvxp4L+Pma91IYi0Yr2rA0R06elC3Eut+IMjH3I8ck49TaVbSSClTou11CkSJCyJ")
response = ProtoBuf(SimplePayPb_pb2).runner(HTTPJSON_IN.prefix+'/plugin/post/simplepay', 'Request', req, flag=0)
result = ProtoBuf(SimplePayPb_pb2).parser('Result', response)
