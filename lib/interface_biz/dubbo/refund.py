#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/7 17:20
# comment:
from case.debug.inland.dubbo.order import Order
from lib.common.file_operation.config_operation import Config
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.env import get_dubbo_info, set_global_env_id
from lib.common_biz.find_database_table import SeparateDbTable
from lib.config.path import common_sql_path
from lib.common.utils.globals import GlobalVar


class Refund:
    def __init__(self):
        dubbo_info = get_dubbo_info("dispatcher")
        self.conn = DubRunner(dubbo_info[0], dubbo_info[1])
        self.order_dubbo = Order()

    def refund_single(self, partnerOrderId, partnerCode, refundAmount, payReqId=''):
        """
        单个订单退款
        :return:
        """
        data = {
            'partnerOrderId': partnerOrderId,
            'notifyUrl': 'www.baidu.com',
            'partnerCode': partnerCode,
            # APPROVE_PROCESS
            'refundType': 'APPROVE_PROCESS',
            'payReqId': payReqId,
            'payType': "",
            'refundAmount': refundAmount,
            'refundId': "",
            "class": "com.keke.dispatcher.inative.entity.SimpleRefundEntity"
        }
        result = self.conn.invoke(
            "IFacade",
            "simpleRefund",
            data
        )

    def refund_by_ssoid(self, ssoid):
        """
        根据ssoid进行批量退款
        :param ssoid:
        :return:
        """
        db_info = SeparateDbTable(ssoid).get_order_db_table()
        sql_refund = str(Config(common_sql_path).read_config("refund", "sql_refund")).format(db_info[0], db_info[1], ssoid)
        mysql = GlobalVar.MYSQL_IN
        refund_list = mysql.select(sql_refund)
        # pay_req_id, amount, partner_order, partner_code, pay_type
        for item in refund_list:
            self.order_dubbo.refund_approval(item['partner_code'], item['partner_order'], str(item['amount']/100), item['pay_type'], item["pay_req_id"])
            self.refund_single(item['partner_order'], item['partner_code'], str(item['amount']/100))
    
    def refund_by_partner_order(self, ssoid, partner_order_id):
        sep_dbtbl = SeparateDbTable(ssoid)
        order_db_info = sep_dbtbl.get_order_db_table()
        del sep_dbtbl
        sql = 'SELECT pay_req_id, amount, partner_order, partner_code, pay_type FROM db_order_{}.order_info_{} WHERE '\
              'STATUS="OK" AND refund=0 AND amount!="0" AND request_time>"2021-01-01 00:00:00" AND partner_order="{}"'.format(
                  order_db_info[0], order_db_info[1], partner_order_id)
        print(sql)
        res = GlobalVar.MYSQL_IN.select_one(sql)
        print(res)
        self.order_dubbo.refund_approval(res['partner_code'], res['partner_order'], str(res['amount']/100), res['pay_type'], res["pay_req_id"])
        self.refund_single(res['partner_order'], res['partner_code'], str(res['amount']/100))
        

if __name__ == '__main__':
    Refund().refund_by_ssoid("2076075925")
    set_global_env_id(1)
#     Refund().refund_by_ssoid("2086100900")
    Refund().refund_by_partner_order("2086100900", 'fa2ddc9c4c334f1ba58c9e544ac74f5e')
    # Refund().refund_single("GC202101241407088040100320000", "5456925", "0.01")
