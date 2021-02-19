#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/19 17:01
# comment:
import time
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.env import get_dubbo_info
from lib.common_biz.order_random import RandomOrder


class Nearme:
    def __init__(self):
        dubbo_info = get_dubbo_info("nearme")
        self.conn = DubRunner(dubbo_info[0], dubbo_info[1])

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


if __name__ == '__main__':
    Nearme().nearme_add_subtract("1", "2076075925", 0)