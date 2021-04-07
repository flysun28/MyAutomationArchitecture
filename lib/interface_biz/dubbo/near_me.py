#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/19 17:01
# comment:
import time
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.env import get_dubbo_info
from lib.common.utils.globals import GlobalVar
from lib.common_biz.order_random import RandomOrder


class Nearme:
    def __init__(self):
        server_info = GlobalVar.ZK_CLIENT_IN.get_node_info("com.oppo.pay.nearme.facade.NearmeAccountOperate")
        self.conn = DubRunner(server_info['ip_port'][0], server_info['ip_port'][1])

    def nearme_add_subtract(self, amount, ssoid, operate_type):
        """
        可币发放扣除
        :param amount: 元 string
        :param ssoid:
        :param operate_type: PRESENT 发放  DEDUCT  扣除
        :return:
        """
        if operate_type in ("P", "PRESENT", "p", "0", 0):
            operate_type = "PRESENT"
        if operate_type in ("D", "DEDUCT", "d", "1", 1):
            operate_type = "DEDUCT"
        data = {
            "amountMoney": str(amount),
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


if __name__ == '__main__':
    flag = "1"
    if flag == "1":
        # 发
        Nearme().nearme_add_subtract("10", "2076075925", 0)
    if flag == "2":
        # 扣
        Nearme().nearme_add_subtract("5", "2076075925", 1)
