#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/7 17:20
# comment:
import time
from itertools import chain
from case.debug.inland.dubbo.order import Order
from lib.common.file_operation.config_operation import Config
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.env import get_dubbo_info, set_global_env_id
from lib.common_biz.find_database_table import SeparateDbTable
from lib.config.path import common_sql_path
from lib.common.utils.globals import GlobalVar
from case.debug.inland.dubbo.order import Order as OrderDubbo
        

class Refund:
    
    def __init__(self, ssoid):
        self.ssoid = ssoid
        self.pay_req_id = None
        self.db_order_info = SeparateDbTable(self.ssoid).get_order_db_table()
        server_info = GlobalVar.ZK_CLIENT_IN.get_node_info("com.keke.dispatcher.inative.facade.IFacade")
        self.conn = DubRunner(server_info['ip_port'][0], server_info['ip_port'][1])
        self.order_dubbo = OrderDubbo()

    def refund_single(self, partnerOrderId, partnerCode, refundAmount, payReqId=''):
        """
        单个订单退款
        :return:
        """
        data = {
            'partnerOrderId': partnerOrderId,
            'notifyUrl': 'http://www.baidu.com',
            'notifyUrl': 'http://pay.pay-test.wanyol.com/notify/notify/receiver',
            'partnerCode': partnerCode,
            # APPROVE_PROCESS
            'refundType': 'APPROVE_PROCESS',
            'payReqId': payReqId,
            'payType': "",
            'refundAmount': refundAmount,
            'refundId': "",
            "class": "com.keke.dispatcher.inative.entity.SimpleRefundEntity"
        }
        self.conn.invoke("IFacade", "simpleRefund", data)

    def refund_by_ssoid(self):
        """
        根据ssoid进行批量退款
        :return:
        """
        sql_refund = str(Config(common_sql_path).read_config("refund", "sql_refund")).format(*self.db_order_info, self.ssoid)
        refund_list = GlobalVar.MYSQL_IN.select(sql_refund)
        # pay_req_id, amount, partner_order, partner_code, pay_type
        for item in refund_list:
            self.order_dubbo.refund_approval(item['partner_code'], item['partner_order'], str(item['amount']/100), item['pay_type'], item["pay_req_id"])
            self.refund_single(item['partner_order'], item['partner_code'], str(item['amount']/100), payReqId=item["pay_req_id"])
    
    def refund_by_partner_order(self, partner_order_id, amount=''):
        sql = 'SELECT pay_req_id, amount, partner_order, partner_code, pay_type FROM pay_tradeorder_{}.trade_order_info_{} WHERE '\
              'STATUS="OK" AND refund=0 AND request_time>"2021-01-01 00:00:00" AND partner_order="{}"'.format(
                  *self.db_order_info, partner_order_id) #+ ' AND refund=0 AND amount!="0"'
        results = GlobalVar.MYSQL_IN.select(sql)
        for res in results:
            refund_amount = str(amount) if amount else str(res['amount']/100)
            self.order_dubbo.refund_approval(res['partner_code'], res['partner_order'], refund_amount, 
                                             res['pay_type'], res["pay_req_id"])
            self.refund_single(res['partner_order'], res['partner_code'], refund_amount, payReqId=res["pay_req_id"])

    def refund_by_amount(self, partner_order_id, amount=''):
        sql = 'SELECT pay_req_id, amount, partner_order, partner_code, pay_type FROM pay_tradeorder_{}.trade_order_info_{} WHERE '\
              'request_time>"2021-01-01 00:00:00" AND partner_order="{}"'.format(
                  *self.db_order_info, partner_order_id) #+ ' AND amount!="0"'
                #((STATUS="OK" AND refund=0) OR (STATUS="REFUNDED" AND refund!=0)) AND 
        results = GlobalVar.MYSQL_IN.select(sql)
        for res in results:
            refund_amount = str(amount) if amount else str(res['amount']/100)
            self.order_dubbo.refund_approval(res['partner_code'], res['partner_order'], refund_amount, res['pay_type'], res["pay_req_id"])
            self.refund_single(res['partner_order'], res['partner_code'], refund_amount, payReqId=res["pay_req_id"])

    def is_on_the_way_refund_existed(self, pay_req_id=''):
        self.pay_req_id = pay_req_id if pay_req_id else self.pay_req_id
        if self.pay_req_id:
            sql = 'SELECT pay_req_id, pay_type, status, refund as 当笔退款金额, pay_amount as 总退款额 FROM db_order_0.refund_info '\
                    'WHERE pay_req_id="%s" AND status="init"' %self.pay_req_id
            res = GlobalVar.MYSQL_IN.select(sql)
            return True if res else False
        return False
    
    def get_sub_partner_orders(self, pay_req_id):
        self.pay_req_id = pay_req_id
        sql = 'SELECT partner_order FROM pay_tradeorder_{}.trade_order_info_{} WHERE pay_req_id="{}"'.format(*self.db_order_info, pay_req_id)
        results = GlobalVar.MYSQL_IN.select(sql)
        return list(chain(*[res.values() for res in results]))
    
    def refund_by_pay_req_id(self, pay_req_id, amount=''):
        for partner_order in self.get_sub_partner_orders(pay_req_id):
            while True:
                if self.is_on_the_way_refund_existed():
                    time.sleep(0.1)
                else:
                    self.refund_by_partner_order(partner_order, amount)
                    break


if __name__ == '__main__':
    Refund().refund_by_ssoid("2076075925")
    set_global_env_id(1)
#     Refund().refund_by_ssoid("2086100900")
    Refund().refund_by_partner_order("2086100900", 'fa2ddc9c4c334f1ba58c9e544ac74f5e')
    # Refund().refund_single("GC202101241407088040100320000", "5456925", "0.01")
