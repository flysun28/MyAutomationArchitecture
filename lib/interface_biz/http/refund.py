# coding=utf-8

import sys
from lib.common_biz.sign import Sign
from lib.common_biz.find_key import GetKey
from lib.common.utils.env import get_env_config
from lib.common.logger.logging import Logger
from lib.common.algorithm.md5 import md5
from lib.common.utils.globals import GlobarVar
from lib.common.exception.http_exception import HttpJsonException

logger = Logger('退款接口', sys.__stdout__).get_logger()


def httpjson_refund(partner_order, partner_code, amount, pay_req_id=None):
    '''
    Currently, only support game-center refund 
    '''
    pay_req_id = pay_req_id if pay_req_id else ''
    req_kwargs = {'partnerOrder': partner_order,
                  'partnerCode': partner_code,
                  'sign': '',
                  'notifyUrl': 'http://pay.pay-test.wanyol.com/notify/notify/receiver',
                  'payReqId': pay_req_id,
                  'refundAmount': amount,
                  'clientIp': ''}
    sign_maker = Sign(req_kwargs)
    key_getter = GetKey(partner_code)
    salt_key = key_getter.get_key_from_merchant()
    orig_sign = sign_maker.join_asc_have_key(salt='&key='+salt_key)
    logger.debug('Sign加密前原始字符串: %s', orig_sign)
    for upper_case in True, False:
        try:
            req_kwargs['sign'] = md5(orig_sign, upper_case)
            logger.info(req_kwargs)
            GlobarVar.HTTPJSON_IN.post('/plugin/post/refund', data=req_kwargs)
            break
        except (HttpJsonException, AssertionError) as e:
            if '签名错误' in e.args[0]:
                continue
            else:
                raise 
    
if __name__ == '__main__':
    httpjson_refund("86c81fd88c2e4a31bdb19ddc023bb559", "2031", "1")
# def httpjson_refund_negative():
            
    

