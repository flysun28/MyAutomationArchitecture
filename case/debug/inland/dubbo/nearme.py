#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/7 15:47
# comment:
import time
from lib.common.logger.logging import Logger
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.env import get_dubbo_info, set_global_env_id
from lib.common_biz.order_random import RandomOrder
logger = Logger("nearme").get_logger()


class Nearme:
    def __init__(self):
        dubbo_info = get_dubbo_info("nearme")
        self.conn = DubRunner(dubbo_info[0], dubbo_info[1])

    def nearme_add_subtract(self, amount, ssoid, operate_type):
        """
        可币发放扣除
        :param amount: 元
        :param ssoid:
        :param operate_type: PRESENT 发放  DEDUCT  扣除
        :return:
        """
        if operate_type in ("P", "PRESENT", "p", "0", 0):
            operate_type = "PRESENT"
        if operate_type in ("D", "DEDUCT", "d", "1", 1):
            operate_type = "DEDUCT"
        data = {
            "amountMoney": amount,
            "batchId": RandomOrder(32).random_num(),
            "bizNo": RandomOrder(32).random_string(),
            "operateType": operate_type,
            "requestId": RandomOrder(32).random_num(),
            "source": "test",
            "ssoid": ssoid,
            "timeStamp": int(round(time.time() * 1000))
        }
        result = self.conn.invoke(
            "NearmeAccountOperate",
            "addSubtractOperate",
            data
        )

    def consume_page_query(self):
        """
        可币消费订单分页查询
        :return:
        """
        data = {
            "page": 1,
            "partnerOrder": "b46d134d6fe44119ad044564eb96d752",
            "size": 10
        }
        result = self.conn.invoke(
            "NearmeOrderQuery",
            "consumePageQuery",
            data
        )
    
    def query_balance(self, ssoid):
        data = {'ssoid': ssoid}
        result = self.conn.invoke('NearmeAccountQuery', 'queryAccountBalance', data, flag='JSON')
        return result['data']['balance']


if __name__ == '__main__':
#     set_global_env_id(3)
#     nearme = Nearme()
#     # 发放可币
#     # nearme.nearme_add_subtract("20.00", "2076075925", 'PRESENT')
# #     # 扣减所有可币余额
#     balance = nearme.query_balance(ssoid='2076075925')
#     nearme.nearme_add_subtract(balance, "2076075925", 'DEDUCT')
#
#     # Nearme().consume_page_query()
    flag = "1"
    if flag == "2":
        # 发
        Nearme().nearme_add_subtract("10", "2076075925", 0)
    if flag == "2":
        # 扣
        Nearme().nearme_add_subtract("5", "2076075925", 1)
