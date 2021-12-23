# coding=utf-8
'''
@author: 80319739
'''
import sys
import time
from itertools import chain
from lib.common_biz.sign import Sign
from lib.common_biz.find_key import GetKey
from lib.common.utils.env import get_env_config, set_global_env_id, get_env_id
from lib.common.logger.logging import Logger
from lib.common.algorithm.md5 import md5
from lib.common.utils.globals import GlobalVar
from lib.common.exception.http_exception import HttpJsonException
from lib.common.exception.intf_exception import ArgumentException
from lib.common.session.http.http_json import HttpJsonSession
from lib.common_biz.find_database_table import SeparateDbTable

logger = Logger('退款接口', sys.__stdout__).get_logger()


class Refund():
    '''查找方法：
    pay-info-dubbo-provider, platform_opay.merchant_info, merchant_id=xxx, system_public_key
    2030业务线是merchant_key
    '''
    partner_private_key = {
        '5456925': 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCmreYIkPwVovKR8rLHWlFVw7YDfm9uQOJKL89Smt6ypXGVdrAKKl0wNYc3/jecAoPi2ylChfa2iRu5gunJyNmpWZzlCNRIau55fxGW0XEu553IiprOZcaw5OuYGlf60ga8QT6qToP0/dpiL/ZbmNUO9kUhosIjEu22uFgR+5cYyQIDAQAB',
        '2031': 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCMVhIN5xQPRdmo1fmm0HBOlRk2XnJsuKgOBi6b1IFAUWtROpm6lRnw45M83a/XiHEZv5FOp+rssGlgwcWeLuexI6kCF5hFT6gsEYy9XRfpSBOUA2UwcajPRsMoEKRmEIm+NpmwnGAeeZK2Y7Xwr3imHdLJ86VgJ5zMedqd4IfXWQIDAQAB',
        '72724314': 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiRRSla2TmY9lVSOa23ab7g61q1LP6wu5j5RiLhnPcaa/cfQncoOo6zflL60AiSCPkWxTWr6aNsvrSQorR3jRDcloqpcgNxVPnrTziZgQiVhWYBgVljbAQAB',
        '7272431402': 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiRRSla2TmY9lVSOa23ab7g61q1LP6wu5j5RiLhnPcaa/cfQncoOo6zflL60AiSCPkWxTWr6aNsvrSQorR3jRDcloqpcgNxVPnrTziZgQiVhWYBgVljbAQAB',
        '247628518': 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCdSq+Wq4WfdLpyM7gVwNOXNXFYSSACoHGzcQ/h5G1ElnL/T4gNCauL2GDMrNvCE6FCOLqI/+Pkewx/1yydvtvaUhCVzqt7zU2CAL35cgx7dicAHhBGTkU6OLLMG1DrETbOsJFUSDpKaMnqjRmtXPH18fWY8I1ExfrZoRtcrQ4yDQIDAQAB',
        '231810428': 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCdSq+Wq4WfdLpyM7gVwNOXNXFYSSACoHGzcQ/h5G1ElnL/T4gNCauL2GDMrNvCE6FCOLqI/+Pkewx/1yydvtvaUhCVzqt7zU2CAL35cgx7dicAHhBGTkU6OLLMG1DrETbOsJFUSDpKaMnqjRmtXPH18fWY8I1ExfrZoRtcrQ4yDQIDAQAB',
        '2030': 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCq7fpWpuV7a4aaORo7Bbs73YZVm+gu2oFwj1lUaHMpXbyFpUPV5tckp/gKRZPkRZ/Wk8Hp/FjpjlG5DRqpMBnlM4CturD26VMOcFudyt6wlbh90glAz0fgaha3gO9Axt2e8gEn7DZw/5ed25HrPLtgaBopnxc9L+yHPqq9Q3v8YwIDAQAB'
    }
    partner_notify_url = {
        '2031': 'http://pay.pay-test.wanyol.com/notify/notify/receiver',
        '72724314': 'http://cn-vip-open.uc.oppo.local/api/pay/purchase-refund-result-notify',
        '5456925': 'http://cnzx-game-test.wanyol.com/sdklocal/pay/refund',
        '9809089': 'http://dgzx-theme-test.wanyol.com/themepay/order/refund'
    }

    def __init__(self, ssoid, http_session=GlobalVar.HTTPJSON_IN):
        self.ssoid = ssoid
        self.partner_order = self.partner_code = None
        self.http_session = http_session
        self.db_order_info = SeparateDbTable(self.ssoid).get_order_db_table()        
    
    def httpjson_refund(self, partner_order, partner_code, amount, pay_req_id=None):
        '''
        amount: 单位元 
        '''
        pay_req_id = pay_req_id if pay_req_id else ''
        req_kwargs = {'partnerOrder': partner_order,
                      'partnerCode': partner_code,
                      'sign': '',
                      'notifyUrl': self.partner_notify_url.get(partner_code, 'http://pay.pay-test.wanyol.com/notify/notify/receiver'),
                      'payReqId': pay_req_id,
                      'refundAmount': amount,
                      'clientIp': ''}
        sign_maker = Sign(req_kwargs)
        key_getter = GetKey(partner_code)
        if get_env_id() in ('grey', 'product'):
            salt_key = self.partner_private_key[partner_code]
        else:
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
        return response
    
    def is_on_the_way_refund_existed(self):
        if self.partner_order:
            sql = 'SELECT pay_req_id, pay_type, status, refund as 当笔退款金额, pay_amount as 总退款额 FROM db_order_0.refund_info '\
                    'WHERE partner_order="%s" AND status="init"' %self.partner_order
            res = GlobalVar.MYSQL_IN.select(sql)            
            return True if res else False
        return False
    
    def get_sub_partner_orders(self, pay_req_id):
        self.pay_req_id = pay_req_id
        sql = 'SELECT partner_order, partner_code FROM pay_tradeorder_{}.trade_order_info_{} WHERE pay_req_id="{}"'.format(*self.db_order_info, pay_req_id)
        results = GlobalVar.MYSQL_IN.select(sql)
        ret = []
        for res in results:
            ret.append(tuple(res.values()))
        return ret
    
    def refund_by_pay_req_id(self, pay_req_id, amount):
        if not pay_req_id:
            return
        for partner_order, partner_code in self.get_sub_partner_orders(pay_req_id):
            while True:
                if self.is_on_the_way_refund_existed():
                    time.sleep(0.1)
                else:
                    self.httpjson_refund(partner_order, partner_code, amount, pay_req_id=pay_req_id)
                    break
    
    def refund_by_ssoid_in_timerange(self, start_time:'YYYY-mm-dd HH:MM:SS', end_time:'YYYY-mm-dd HH:MM:SS'='', ssoid=None):
        db_order_info = SeparateDbTable(ssoid).get_order_db_table() if ssoid else self.db_order_info
        try:
            print(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
        except:
            raise ValueError('Invalid `start_time`:{}, should be formatted as YYYY-mm-dd HH:MM:SS'.format(start_time))
        if not end_time:
            end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) or 'CURRENT_TIMESTAMP'
        sql = 'SELECT partner_code,partner_order,amount,pay_type,pay_req_id FROM pay_tradeorder_{}.trade_order_info_{} WHERE status="OK" AND refund=0 AND success_time>="{}" AND success_time<="{}"'.format(*db_order_info, start_time, end_time)
        results = GlobalVar.MYSQL_IN.select(sql)
        for res in results:
            refund_amount = str(res['amount']/100)
            self.httpjson_refund(res['partner_order'], res['partner_code'], refund_amount)


if __name__ == '__main__':
    set_global_env_id(3)
    refund = Refund('2086100900')
    # 全额退款
    refund.refund_by_pay_req_id('RM202104261036302086776969622522', 0.01)
    # 部分退款
    per_amount = 1
    total_amount = 5
    loop_num = int(total_amount/per_amount)
    for partner_order, partner_code in refund.get_sub_partner_orders('KB202103111508592086100900248122'):
        for i in range(loop_num):
            while True:
                if refund.is_on_the_way_refund_existed():
                    time.sleep(0.1)
                else:
                    refund.httpjson_refund(partner_order, partner_code, per_amount, pay_req_id='')
                    break

    
    

