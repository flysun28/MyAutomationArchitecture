'''
Created on 2021年5月31日
@author: 80319739
'''
import random
from lib.interface_biz.http.pay_pass import get_process_token
from lib.common.utils.globals import GlobalVar, HTTPENCJSON_IN
from lib.common_biz.order_random import RandomOrder

# 所有金额的单位均为分

goodsType = 'COMMON'
screenInfo = random.choice(['FULL', 'HALF', 'ACROSS_SCREEN'])
req = {
    # mandatory
    "processToken": get_process_token(),
    'payType': 'VIRTUAL_ASSETS',  # 支付渠道, 银行卡支付 BANK_CARD, 虚拟支付 VIRTUAL_ASSETS 
    'goodsType': goodsType,    # 商品类型 COCOIN/COMMON
    'platform': 'ATLAS',       # SDK类型: MSP ATLAS(安全支付)
    "partnerCode": "2031",
    'partnerOrder': RandomOrder(32).random_string() if goodsType == 'COMMON' else '',
    'amount': 1,    # 原始金额
    'productName': 'test direct pay',    # 商品名称
    'productDesc': 'test direct pay',    # 商品描述
    'notifyUrl': GlobalVar.URL_PAY_IN+"/notify/receiver",    #支付结果通知地址
    'clientCallbackUrl': '1',  #客户端回调地址
    'price': 1,    # number    价格    
    'count': 1,    # number    数量    
    'screenInfo': screenInfo,    # FULL, HALF, ACROSS_SCREEN
    # optional
    'currencyCode': '',    # 货币编码
    'currencyName': '',    # 货币名称
    'source': '',
    'appPackage': '',    # 业务包名
    'appVersion': '',    # 业务版本号
    'appId': '',         # MSP需要传递 APPID
    'partnerSign':'',    # 业务方签名
    'channelId': '', 
    'factor': '',
    'discountCode': '',
    'acqAddnData': '',
    'attach': '',   # 业务透传扩展字段
    'ext': '',      # 支付扩展字段
    # 可币、可币券
#     'virtualAssets': {
#         'cocoinDeductAmount': 0,    # number  可币抵扣金额
#         'voucherId': '',            # 可币券ID
#         'voucherType': 0,           # number  可币券类型
#         'voucherDeductAmount': 0,   # number  可币券抵扣金额
#         'virtualVoucher': '',       # 取值 Y/N, 是否为虚拟券
#         'cocoinCount': '',          # 可币数量, 支持小数
#         'creditCount': 0,           # number
#         'creditDeductAmount': 0     # number  积分抵扣金额
#     },
#     # 加购商品
#     'combineOrder': {
#         'buyPlaceId': '',   # 加购位ID
#         'amount': 0         # number  加购商品金额
#     },
    'token': '',    # 用户Token
    'currencySystem': 'CASH',    # 枚举值 COCOIN, CASH
    # 充值卡信息 
#     'rechargeCard': {
#         'cardNo': '',
#         'cardPwd': '',
#         'cardAmount': ''
#     }
}

result = HTTPENCJSON_IN.post('/api/pay-flow/v290/pay', req)
print(result)

