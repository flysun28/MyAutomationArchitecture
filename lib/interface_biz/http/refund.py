# coding=utf-8
'''
@author: 80319739
'''
import sys
import time
from lib.common_biz.sign import Sign
from lib.common_biz.find_key import GetKey
from lib.common.utils.env import get_env_config, set_global_env_id
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
            logger.info('退款请求报文: %s', req_kwargs)
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
    session = HttpJsonSession('https://pre-nativepay.keke.cn')
    set_global_env_id(3)
    refund = Refund()
    per_amount = 0.01
    total_amount = 0.01
    loop_num = int(total_amount/per_amount)
    for i in range(loop_num):
        while True:
            if refund.is_on_the_way_refund_existed():
                time.sleep(0.1)
            else:
                refund.httpjson_refund("610306f201b84ecd9bf8beb834b3ecdc", "5456925", per_amount, pay_req_id='')
#                 refund.httpjson_refund("JG202103082126042086100900703477", "72724314", per_amount, pay_req_id='')
                break

    
    

