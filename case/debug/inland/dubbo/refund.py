#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/7 17:20
# comment:
from case.debug.inland.dubbo.order import Order
from lib.common.file_operation.config_operation import Config
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.env import get_dubbo_info
from lib.common_biz.find_database_table import SeparateDbTable
from lib.common_biz.order_random import RandomOrder
from lib.config.path import common_sql_path
from lib.common.utils.globals import GlobarVar




class Refund:
    def __init__(self):
        dubbo_info = get_dubbo_info("dispatcher")
        self.conn = DubRunner(dubbo_info[0], dubbo_info[1])

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
        sql_refund = str(Config(common_sql_path).read_config("refund", "sql_refund")).format(db_info[0], db_info[1],
                                                                                             ssoid)
        mysql = GlobarVar.MYSQL_IN
        refund_list = mysql.select(sql_refund)
        # pay_req_id, amount, partner_order, partner_code, pay_type
        for item in refund_list:
            Order().refund_approval(item['partner_code'], item['partner_order'], str(item['amount']/100), item['pay_type'],
                                    item["pay_req_id"])
            self.refund_single(item['partner_order'], item['partner_code'], str(item['amount']/100))


if __name__ == '__main__':
    Refund().refund_by_ssoid("2000062087")
    # Refund().refund_single("GC202101241407088040100320000", "5456925", "0.01")
