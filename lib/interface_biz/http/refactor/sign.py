'''
Created on 2021年6月16日
@author: 80319739
'''
import re
import random
from lib.common.utils.globals import GlobalVar, HTTPENCJSON_IN, HTTPJSON_API_IN
from lib.interface_biz.http.pay_pass import get_process_token
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.biz_db_operate import get_renew_product_code


class SignPayGWClient():
    
    def __init__(self, partner_id='2031'):
        renew_product_code = get_renew_product_code(partner_id)
        '''
        processToken        string            非必须            processToken（processToken，第三方id必传一个）    
        thirdPartId        string             非必须            第三方id（processToken，第三方id必传一个）    
        renewProductCode    string            必须            签约产品代码    
        partnerCode        string             必须            业务线id    
        signPartnerOrder    string            必须            签约订单号    
        appPackage        string              必须            业务方包名    
        appVersion        string              非必须          业务方版本号
        payType            string             必须            支付方式 alipay wxpay    
        notifyUrl        string               必须            支付结果通知地址
        country            string             必须            国家 CN
        currency        string                必须            货币编码 CNY
        transType        string               必须            签约SIGN 签约并支付SIGNANDPAY
        subUserId        string               非必须            子用户id
        subUserName       string             非必须            子用户姓名
        amount            integer            非必须            金额，单位分（签约并支付必须）
        subject            string            非必须            商品名称（签约并支付必须）
        desc                string           非必须            商品描述（签约并支付必须）
        partnerOrder        string           非必须            业务订单号（签约并支付必须）
        screenInfo        string             非必须            屏幕信息 FULL, HALF, ACROSS
        '''    
        self.post_req = {
            # mandatory
            'renewProductCode': renew_product_code,
            'partnerCode': partner_id,
            'signPartnerOrder': RandomOrder(32).random_string(),
            'appPackage': 'com.example.pay_demo',
            'notifyUrl': GlobalVar.URL_PAY_IN+"/notify/receiver",    #支付结果通知地址
            'country': 'CN',
            'currency': 'CNY',
            'transType': '',
            'payType': '',
            # optional
            'processToken': get_process_token(),
            'thirdPartId': '',
            'appVersion': '',
            'subUserId': '',
            'subUserName': '',
            'amount': 0,
            'subject': '',
            'desc': '',
            'partnerOrder': '',
            'screenInfo': random.choice(['FULL', 'HALF', 'ACROSS']),    # FULL, HALF, ACROSS
        }
        self.query_req = {
            'payRequestId': '',
            'transType': ''
        }

        self.post_result = {}

    def sign_and_pay(self, amount, pay_type):
        req = self.post_req.copy()
        req['transType'] = 'SIGNANDPAY'
        self._post(req, amount, pay_type)
    
    def sign_only(self, pay_type, amount=0):
        req = self.post_req.copy()
        req['transType'] = 'SIGN'
        self._post(req, amount, pay_type)
    
    def sign_and_pay_negative(self, amount=None, pay_type=None, **kwargs):
        req = self.post_req.copy()
        req['transType'] = 'SIGNANDPAY'
        pay_type = pay_type if pay_type else kwargs.get('payType')
        req.update(kwargs)
        self._post(req, amount, pay_type, **kwargs)
    
    def sign_only_negative(self, pay_type, **kwargs):
        req = self.post_req.copy()
        req['transType'] = 'SIGN'
        req.update(kwargs)
        self._post(req, kwargs.get('amount', 0), pay_type, **kwargs)
       
    def query_sign_result(self, pay_req_id=None, pay_type=None):
        req = self.query_req.copy()
        if self.post_result:
            pay_req_id = pay_req_id if pay_req_id else self.post_result['data']['payRequestId']
            pay_type = pay_type if pay_type else self._pay_type_from_response()
        else:
            assert pay_req_id and pay_type, 'Both payRequestId and transType should not be empty!'
        req.update(payRequestId=pay_req_id, 
                   transType=pay_type)
        result = HTTPENCJSON_IN.post('/api/autorenew/v290/query-result', req)
        del req
        return result
    
    def unsign_negative(self, agreement_no, pay_type, partner_order, **kwargs):
        pass
    
    def _post(self, req, amount, pay_type, **kwargs):
        req['payType'] = pay_type or kwargs.get('payType')
        req['amount'] = kwargs.get('amount', 0) if amount is None else amount
#         req['subject'] = '签约并支付商品名称'
#         req['desc'] = '签约并支付商品描述'
        req['subject'] = 'test product subject' if kwargs.get('subject', None) is None else kwargs['subject']
        req['desc'] = 'test product description' if kwargs.get('desc', None) is None else kwargs['desc']
        self.post_result = HTTPENCJSON_IN.post('/api/autorenew/v290/sign-and-pay', req)
        del req

    def _pay_type_from_response(self):
        pay_type = re.search('\w+pay', self.post_result['data']['channelData'], re.I).group().lower()
        print('支付方式（渠道）:', pay_type)
        return pay_type


class SignPayGWApi():
    
    def __init__(self, partner_id='2031'):
        renew_product_code = get_renew_product_code(partner_id)
        '''
        renewProductCode   string           必须        签约产品代码
        partnerOrder       string           必须        业务订单号
        notifyUrl          string           必须        签约结果通知地址
        payType            string           必须        支付方式 alipay wxpay
        ssoid              string           必须        用户id
        subUserId          string           非必须      子用户id
        partnerCode        string           必须        业务线ID
        agreementNo        string           必须        协议号
        amount             string           必须        支付金额，单位元
        subject            string           必须        产品名称
        '''
        self.autorew_req = {
            # mandatory
            'renewProductCode': renew_product_code,
            'partnerOrder': RandomOrder(32).random_string(),
            'notifyUrl': GlobalVar.URL_PAY_IN+"/notify/receiver",    #支付结果通知地址
            'payType': '',
            'ssoid': GlobalVar.SSOID,
            'partnerCode': partner_id,
            'agreementNo': '',
            'amount': 0,
            'subject': 'test auto renew!~^(&#*@~%$)&%-=_+{}[]|\:";,./<>?`',
            'subject': 'test auto renew',
            # optional
            'subUserId': '',    #仅保险 子账户
        }
        '''
        renewProductCode   string           必须        签约产品代码
        partnerOrder       string           必须        业务订单号
        partnerCode        string           必须        业务线ID
        ssoid              string           必须        用户id
        payType            string           必须        支付方式 alipay wxpay
        agreementNo        string           必须        协议号
        subUserId          string           非必须      子用户id
        '''
        self.unsign_req = {
            # mandatory
            'renewProductCode': renew_product_code,
            'partnerOrder': '',            
            'partnerCode': partner_id,
            'ssoid': GlobalVar.SSOID,
            'payType': '',
            'agreementNo': '',
            # optional
            'subUserId': '',    #仅保险 子账户
        }

    def autorenew(self, agreement_no, pay_type, amount):
        req = self.autorew_req.copy()
        req.update(agreementNo=agreement_no, payType=pay_type, amount=amount)
        result = HTTPJSON_API_IN.post('/api/autorenew/v1/autopay', req)
        del req
        return result
    
    def autorenew_negative(self, agreement_no, pay_type, amount, **kwargs):
        req = self.unsign_req.copy()
        self.autorenew(agreement_no, pay_type, amount)
        
    def unsign(self, agreement_no, pay_type, partner_order):
        req = self.unsign_req.copy()
        req.update(agreementNo=agreement_no, payType=pay_type, partnerOrder=partner_order)
        result = HTTPJSON_API_IN.post('/api/autorenew/v1/unsign', req)
        del req
        return result

    def _post(self, req, **kwargs):
        req.update(kwargs)

