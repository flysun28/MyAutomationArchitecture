'''
Created on 2021年5月31日
@author: 80319739
'''
import random
from copy import deepcopy
from lib.interface_biz.http.pay_pass import get_process_token
from lib.common.utils.globals import GlobalVar, HTTPENCJSON_IN
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.biz_db_operate import get_available_voucher
from lib.common_biz.voucher_calculation import VouCalculator
from lib.common.utils.misc_utils import to_pinyin, is_all_chinese
from lib.interface_biz.dubbo.near_me import Nearme
from lib.common.utils.constants import voucher_type_mapping, app_packages, voucher_enum_to_type


class Pay():    
    
    def __init__(self, partner_id='2031', ssoid=GlobalVar.SSOID):
        self.partner_id = partner_id
        self.vou_calc = VouCalculator()
        self.strategy = None
        self.nearme = Nearme(ssoid)
        # 所有金额的单位均为分
        self.req = {            
            # mandatory
            "processToken": get_process_token(),
            'payType': '',  # 支付渠道, 银行卡支付 BANK_CARD, 虚拟支付 VIRTUAL_ASSETS, wxpay, alipay
            'goodsType': '',    # 商品类型 COCOIN/COMMON，COCOIN：纯充值 COMMON：充值并消费
            'platform': 'ATLAS',       # SDK类型: MSP ATLAS(安全支付)
            "partnerCode": self.partner_id,
            'partnerOrder': '',
            'amount': 0,    # 原始金额
            'productName': '重构-网关下单新接口',    # 商品名称
            'productDesc': '重构-网关下单新接口',    # 商品描述
            'productName': 'test',    # 商品名称
            'productDesc': 'test pay',    # 商品描述
            'notifyUrl': GlobalVar.URL_PAY_IN+"/notify/receiver",    #支付结果通知地址
            'clientCallbackUrl': '',  #客户端回调地址
            'price': 0,    # number    价格（单价），price*count=amount
            'count': 1,    # number    数量，固定为1
            'screenInfo': random.choice(['FULL', 'HALF', 'ACROSS']),    # FULL, HALF, ACROSS
            'currencyCode': 'CNY',    # 货币编码
            # optional
            'currencyName': '',    # 货币名称
            'source': '',
            'appPackage': random.choice(app_packages),    # 业务包名
            'appVersion': '',    # 业务版本号
            'appId': '',         # MSP需要传递 APPID
            'partnerSign':'',    # 业务方签名
            'channelId': '', 
            'factor': '',
            'discountCode': '',
            'acqAddnData': '',
            'attach': '',   # 业务透传扩展字段
            'ext': '',      # 支付扩展字段
            'token': '',    # 用户Token
            'currencySystem': '',    # 枚举值 COCOIN_ALLOWED, CASH（直扣）
            'country': 'CN',
            # 可币、可币券
            'virtualAssets': {
                'cocoinCount': '',          # 可币数量, 支持小数。原始可币扣减额
                'cocoinDeductAmount': 0,    # number  可币抵扣金额，针对海外有汇率
                'voucherId': '',            # 可币券ID
                'voucherCount': '',         # 可币券数量
                'voucherType': 0,           # number  可币券类型
#                 'voucherDeductAmount': 0,   # number  可币券抵扣金额
                'virtualVoucher': '',       # 取值 Y/N, 是否为虚拟券
                'creditCount': 0,           # number
                'creditDeductAmount': 0     # number  积分抵扣金额
            },
            # 加购商品
            'combineOrder': {
                'buyPlaceId': '',   # string，加购位ID，非必须
                'amount': 0,         # number  加购商品金额，非必须
                'renewProductCode': '', # string，非必须
                'signNotifyUrl': '',    # string，非必须
                'transType': '',    # string，支付类型，非必须
                'desc': '',         # string，商品名称，非必须
                'subject': ''       # string，商品描述，非必须
            },
#             # 充值卡信息 
#             'rechargeCard': {
#                 'cardNo': '',
#                 'cardPwd': '',
#                 'cardAmount': 0
#             }
        }
        
    def combine_pay(self, amount, buy_place_id=''):
        

    def direct_pay(self, orig_amount, pay_type, partner_order=''):
        '''
        直扣，当前渠道仅支持微信、支付宝
        :param orig_amount: 单位分
        :param pay_type: alipay, wxpay
        '''
        req = deepcopy(self.req)
        req['goodsType'] = 'COMMON'
        req['payType'] = pay_type
        req['partnerOrder'] = partner_order or (RandomOrder(32).random_string() if req['goodsType'] == 'COMMON' else '')
        req['currencySystem'] = random.choice(['CASH', 'COCOIN_ALLOWED'])
        req['amount'] = req['price'] = orig_amount
#         req['productDesc'] += '直扣-'+pay_type
        req['productDesc'] += 'direct pay-'+pay_type
#         req.pop('virtualAssets')
        result = HTTPENCJSON_IN.post('/api/pay-flow/v290/pay', req)
        del req
        return result
    
    def direct_pay_with_kb_negative(self, orig_amount, pay_type, vou_key=None, kb_spent=None, **neg_kw):
        req = self._create_req_with_channel_common(orig_amount, pay_type, **neg_kw)
        req['currencySystem'] = 'CASH'
        if vou_key:
            vou_deduct_amount = self._make_voucher_args(req, orig_amount, vou_key, None, **neg_kw)
            print('实付金额(分):', orig_amount-vou_deduct_amount)
        if kb_spent:
            self._make_cocoin_args(req, kb_spent)
            print('实付金额(分):', orig_amount-kb_spent)
        result = HTTPENCJSON_IN.post('/api/pay-flow/v290/pay', req)
        del req
        return result

    def only_kb_spend(self, orig_amount):
        '''
        仅可币
        :param orig_amount: 单位分
        '''
        req = self._create_req_with_kb_common(orig_amount)
#         req['productDesc'] += ' 纯消费-可币'
        self._make_cocoin_args(req, orig_amount)
        req['productDesc'] += ' only cocoin spend'
        result = HTTPENCJSON_IN.post('/api/pay-flow/v290/pay', req)
        del req
        print('可币余额(分)：', int(self.nearme.query_balance()*100))
        return result

    def only_voucher_spend(self, orig_amount:int, vou_key:str, vou_deduct_amount=None, **vou_kw):
        '''
        仅优惠券
        :param orig_amount: 单位分
        :param vou_key: 中文或对应拼音, [消费 抵扣 折扣 消费折扣 红包]
        :param vou_deduct_amount: 单位分，为None时，会根据原始金额自动计算抵扣额度，规则如下：
        1. 消费券： maxAmount为面额
        2. 抵扣券：满maxAmount，减amount
        3. 折扣券：最低消费amount，单笔最高减maxAmount，ext为折扣
        4. 消费折扣券：同折扣券，usable_amt为剩余额度
        '''
        req = self._create_req_with_kb_common(orig_amount)
#         req['productDesc'] += ' 纯消费-可币券'
        self._make_voucher_args(req, orig_amount, vou_key, vou_deduct_amount, **vou_kw)
        req['productDesc'] += ' only voucher spend'
        result = HTTPENCJSON_IN.post('/api/pay-flow/v290/pay', req)
        del req
        return result
    
    def only_kb_voucher_spend(self, orig_amount:int, vou_key:str, vou_deduct_amount=None, kb_spent=None):
        req = self._create_req_with_kb_common(orig_amount)
        vou_deduct_amount = self._make_voucher_args(req, orig_amount, vou_key, vou_deduct_amount)
        if kb_spent is None:
            kb_spent = orig_amount - vou_deduct_amount
        self._make_cocoin_args(req, kb_spent)
        req['productDesc'] += ' only cocoin+voucher spend'
        result = HTTPENCJSON_IN.post('/api/pay-flow/v290/pay', req)
        del req
        return result
    
    def channel_kb_pay(self, orig_amount, pay_type, kb_spent=None):
        req = self._create_req_with_channel_common(orig_amount, pay_type)
        if kb_spent is None:
            kb_spent = int(self.nearme.query_balance() * 100)
        self._make_cocoin_args(req, kb_spent)
        print('实付金额(分):', orig_amount-kb_spent)
        result = HTTPENCJSON_IN.post('/api/pay-flow/v290/pay', req)
        del req
        return result

    def channel_voucher_pay(self, orig_amount, pay_type, vou_key, vou_deduct_amount=None, **kwargs):
        req = self._create_req_with_channel_common(orig_amount, pay_type)
        vou_deduct_amount = self._make_voucher_args(req, orig_amount, vou_key, vou_deduct_amount, **kwargs)
        print('实付金额(分):', orig_amount-vou_deduct_amount)
        result = HTTPENCJSON_IN.post('/api/pay-flow/v290/pay', req)
        del req
        return result

    def channel_kb_voucher_pay(self, orig_amount, pay_type, vou_key, vou_deduct_amount=None, kb_spent=None, partner_order=''):
        req = self._create_req_with_channel_common(orig_amount, pay_type, partner_order)
        vou_deduct_amount = self._make_voucher_args(req, orig_amount, vou_key, vou_deduct_amount)
        if kb_spent is None:
            kb_spent = int(self.nearme.query_balance() * 100)
        self._make_cocoin_args(req, kb_spent)
        print('实付金额(分):', orig_amount-vou_deduct_amount-kb_spent)
        result = HTTPENCJSON_IN.post('/api/pay-flow/v290/pay', req)
        del req
        return result
    
    def recharge(self, orig_amount, pay_type):
        '''
        goodsType=COCOIN
        '''
        req = self._create_req_with_channel_common(orig_amount, pay_type, is_recharge=True)
        req.pop('virtualAssets')
        print('实付金额(分):', orig_amount)
        result = HTTPENCJSON_IN.post('/api/pay-flow/v290/pay', req)
        del req
        return result
        
    def recharge_with_kb_negative(self, orig_amount, pay_type, vou_key=None, kb_spent=None, **neg_kw):
        req = self._create_req_with_channel_common(orig_amount, pay_type, is_recharge=True, **neg_kw)
        if vou_key:
            vou_deduct_amount = self._make_voucher_args(req, orig_amount, vou_key, None, **neg_kw)
            amount = orig_amount - vou_deduct_amount
            print('可币券优惠后，实付金额(分):', amount)
        if kb_spent:
            self._make_cocoin_args(req, kb_spent)
            amount = locals().get('amount', orig_amount) - kb_spent
            print('抵扣可币后，实付金额(分):', amount)
        result = HTTPENCJSON_IN.post('/api/pay-flow/v290/pay', req)
        del req
        return result    
    
    def _create_req_with_kb_common(self, orig_amount):
        req = deepcopy(self.req)
        req['goodsType'] = 'COMMON'
        req['payType'] = 'VIRTUAL_ASSETS'
        req['currencySystem'] = 'COCOIN_ALLOWED'
        req['partnerOrder'] = RandomOrder(32).random_string() if req['goodsType'] == 'COMMON' else ''
        req['amount'] = req['price'] = orig_amount
        return req
    
    def _create_req_with_channel_common(self, orig_amount, pay_type, partner_order='', is_recharge=False, **neg_kw):
        req = deepcopy(self.req)
        if is_recharge:
            req['goodsType'] = 'COCOIN'
            req['currencySystem'] = 'CASH'
        else:
            req['goodsType'] = 'COMMON'
            req['currencySystem'] = 'COCOIN_ALLOWED'
        req['payType'] = pay_type
        req['partnerOrder'] = partner_order or RandomOrder(32).random_string() if req['goodsType'] == 'COMMON' else ''
        req['amount'] = req['price'] = orig_amount
        req.update(neg_kw)
        return req
    
    def _set_strategy(self, vou_type:str)-> VouCalculator.strategy:
        if is_all_chinese(vou_type):
            vou_type = to_pinyin(vou_type)
        self.vou_calc.strategy = vou_type
        self.strategy = self.vou_calc.strategy

    def _calculate_voucher_deduct(self, orig_amount)-> int:
        return int(self.strategy(orig_amount))
    
#     def _make_voucher_args(self, req, orig_amount, vou_type, vou_deduct_amount):
#         if vou_deduct_amount is None:
#             self._set_strategy(vou_type)
#             vou_deduct_amount = self._calculate_voucher_deduct(orig_amount)
#             db_vou_info = self.vou_calc.vou_info
#         else:
#             db_vou_info = get_available_voucher(GlobalVar.SSOID, vou_type)
#         print('本次支付将使用的可币券:', db_vou_info)
#         print('可币券优惠金额(分):', vou_deduct_amount)
#         req['virtualAssets']['voucherId'] = db_vou_info['vouId']
#         req['virtualAssets']['voucherType'] = voucher_type_mapping[db_vou_info['type']]
#         req['virtualAssets']['voucherDeductAmount'] = vou_deduct_amount
#         if to_pinyin(vou_type) == 'xiaofei':
#             req['virtualAssets']['voucherCount'] = int(orig_amount / vou_deduct_amount)
#         else:
#             req['virtualAssets']['voucherCount'] = 1
#         return vou_deduct_amount
    
    def _make_voucher_args(self, req, orig_amount, vou_key, vou_deduct_amount, **vou_kw):
        '''
        构造可币券相关参数
        :param req:
        :param orig_amount:
        :param vou_key: 券id，或者券类型（中文，英文，数字）
        :param vou_deduct_amount:
        '''
        db_vou_info = get_available_voucher(GlobalVar.SSOID, vou_key)
        self.vou_calc.vou_info = db_vou_info
        vou_type = self._to_vou_type(vou_key, db_vou_info)
        self._set_strategy(vou_type)
        if vou_deduct_amount is None:
            vou_deduct_amount = self._calculate_voucher_deduct(orig_amount)
        print('本次支付将使用的可币券:', db_vou_info)
        print('可币券优惠金额(分):', vou_deduct_amount)
        req['virtualAssets']['voucherType'] = voucher_type_mapping[db_vou_info['type']]
        req['virtualAssets']['voucherDeductAmount'] = vou_deduct_amount
        if to_pinyin(vou_type) == 'xiaofei':
            if vou_kw.get('voucherCount') is None:
                req['virtualAssets']['voucherCount'] = int(orig_amount / vou_deduct_amount)
            req['virtualAssets']['voucherId'] = '0'
        else:
            req['virtualAssets']['voucherCount'] = 1
            req['virtualAssets']['voucherId'] = db_vou_info['vouId']
        req['virtualAssets'].update(vou_kw)
        return vou_deduct_amount
    
    def _make_cocoin_args(self, req, kb_spent:int):
        print('可币抵扣金额(分):', kb_spent)
        req['virtualAssets']['cocoinDeductAmount'] = kb_spent
        req['virtualAssets']['cocoinCount'] = kb_spent
    
    @staticmethod
    def _to_vou_type(vou_key:(str, int), db_vou_info:dict):
        vou_key = str(vou_key)  
        if vou_key.isdigit():
            if len(vou_key) > 2:
                vou_type = voucher_enum_to_type[db_vou_info['type']]
            else:
                vou_type = voucher_enum_to_type[vou_key]
        else:
            vou_type = vou_key
        return vou_type


def update_voucher_args(req, vou_key):
    db_vou_info = get_available_voucher(GlobalVar.SSOID, vou_key)    
    vou_type = Pay._to_vou_type(vou_key, db_vou_info)
    print('本次支付将使用的可币券:', db_vou_info)
    req['virtualAssets']['voucherType'] = voucher_type_mapping[db_vou_info['type']]
    if to_pinyin(vou_type) == 'xiaofei':
#         if vou_kw.get('voucherCount') is None:
#             req['virtualAssets']['voucherCount'] = int(orig_amount / vou_deduct_amount)
        req['virtualAssets']['voucherId'] = '0'
    else:
#         req['virtualAssets']['voucherCount'] = 1
        req['virtualAssets']['voucherId'] = db_vou_info['vouId']

