'''
Created on 2021年8月24日
@author: 80319739
'''
from lib.common.db_operation.redis_operation import connect_redis
from lib.common.utils.globals import MYSQL_IN, MYSQL_OUT


class CreditInfo():
    
    def __init__(self, in_out='inland'):
        self.redis_conn = connect_redis(in_out)
        self.mysql = MYSQL_IN if in_out == 'inland' else MYSQL_OUT
    
    def get_used_credit(self, ssoid, date:'YYYYMMDD'):
        return self.redis_conn.get('pay_biz_paycenter:credit_day_limit:{}:{}'.format(date, ssoid))
    
    def get_current_deduct_amount(self, partner_order):
        return self.redis_conn.get('pay_gateway_client:credit_info:partner_order:'+partner_order)
    
    def get_strategy(self, partner_id, strategy_name):
        '''
        :param partner_id:
        :param strategy_name:
            credit_pay_deduct_rate            多少积分抵扣1分钱
            deduct_credit_count_day_limit    积分每日限额
            single_pay_amount                使用积分抵扣的订单条件金额
            single_pay_deduct_rate_limit    积分最高抵扣订单金额
        '''
        sql = 'SELECT * FROM platform_opay.credit_strategy WHERE partner_code="%s" AND strategy_name=%s;' %(partner_id, strategy_name)
        self.mysql.select(sql)