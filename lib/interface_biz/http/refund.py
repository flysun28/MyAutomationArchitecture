# coding=utf-8
'''
@author: 80319739
'''
import sys
import time
from lib.common_biz.sign import Sign
from lib.common_biz.find_key import GetKey
from lib.common.utils.env import get_env_config
from lib.common.logger.logging import Logger
from lib.common.algorithm.md5 import md5
from lib.common.utils.globals import GlobarVar
from lib.common.exception.http_exception import HttpJsonException
from lib.common.exception.intf_exception import ArgumentException
from lib.common.session.http.http_json import HttpJsonSession

logger = Logger('退款接口', sys.__stdout__).get_logger()


class Refund():
    
    def __init__(self, http_session=GlobarVar.HTTPJSON_IN):
        self.partner_order = self.partner_code = None
        self.http_session = http_session
    
    def httpjson_refund(self, partner_order, partner_code, amount, pay_req_id=None):
        '''
        amount: 单位元 
        '''
        pay_req_id = pay_req_id if pay_req_id else ''
        req_kwargs = {'partnerOrder': partner_order,
                      'partnerCode': partner_code,
                      'sign': '',
                      'notifyUrl': 'http://pay.pay-test.wanyol.com/notify/notify/receiver',
#                     'notifyUrl': 'http://cn-vip-open.uc.oppo.local/api/pay/purchase-refund-result-notify',    # 通知会员地址
                      'payReqId': pay_req_id,
                      'refundAmount': amount,
                      'clientIp': ''}
        sign_maker = Sign(req_kwargs)
        key_getter = GetKey(partner_code)
        salt_key = key_getter.get_key_from_merchant()
        orig_sign = sign_maker.join_asc_have_key(salt='&key='+salt_key)
        logger.info('Sign加密前原始字符串: %s', orig_sign)
        for upper_case in False, True:
            req_kwargs['sign'] = md5(orig_sign, upper_case)
            logger.info(req_kwargs)
            response = self.http_session.post('/plugin/post/refund', data=req_kwargs)
            if '签名错误' == response['resMsg']:
                continue
            break
        self.partner_order = partner_order
        self.partner_code = partner_code
    
    def is_on_the_way_refund_existed(self):
        if self.partner_order:
            sql = 'SELECT pay_req_id, pay_type, status, refund as 当笔退款金额, pay_amount as 总退款额 FROM db_order_0.refund_info '\
                    'WHERE partner_order="%s" AND status="init"' %self.partner_order
            res = GlobarVar.MYSQL_IN.select(sql)            
            return True if res else False
        return False


if __name__ == '__main__':
    # session = HttpJsonSession('https://pre-nativepay.keke.cn')
    refund = Refund()
    per_amount = 0.01
    total_amount = 0.01
    loop_num = int(total_amount/per_amount)
    for i in range(loop_num):
        while True:
            if refund.is_on_the_way_refund_existed():
                time.sleep(0.1)
            else:
                refund.httpjson_refund("288f0ff4e3ab4c6a9b22d2aefb5290d4", "2031", per_amount)
                break

    
    

