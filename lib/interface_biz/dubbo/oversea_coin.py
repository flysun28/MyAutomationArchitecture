#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2020/9/3 14:25
# comment: 可币发放与扣除
from lib.common.logger.logging import Logger
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.env import get_dubbo_info
from lib.common.utils.globals import GlobalVar
from lib.common_biz.order_random import RandomOrder

logger = Logger('oversea_cocoin').get_logger()


class Coin:
    def __init__(self):
        server_info = GlobalVar.ZK_CLIENT_OUT.get_node_info("com.oppo.cocoin.facade.CocoinAccountOperationFacade")
        self.conn = DubRunner(server_info['ip_port'][0], server_info['ip_port'][1])

    def cocoin_in_come(self, ssoid, country, amount):
        """
        可币发放
        :return:
        """
        conn = DubRunner('10.3.1.77', 20900)
        data = ssoid, country, str(amount), "TEST"
        result = conn.invoke(
            "CocoinAccountOperationFacade",
            "income",
            data,
            "STRING"
        )

    def cocoin_pay_out(self, ssoid, country, amount):
        """
        扣除可币余额
        :return:
        """
        conn = DubRunner('10.3.1.77', 20900)
        data = ssoid, country, amount, "TEST"
        result = conn.invoke(
            "CocoinAccountOperationFacade",
            "payout",
            data,
            "STRING"
        )


if __name__ == '__main__':
    Coin().cocoin_in_come("2076075925", "VN", "1")
#     nearme_add_subtract('10.177.159.14', "0.03", "2086100900", "DEDUCT")    #test3
#     nearme_add_subtract('10.177.110.171', "1", "2086100900", "PRESENT")     #test1
#     nearme_add_subtract('10.177.110.171', "6", "2086100900", "DEDUCT")

