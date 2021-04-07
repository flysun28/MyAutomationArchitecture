#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/7 14:26
# comment:
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.logger.logging import Logger
from lib.common.utils.env import get_dubbo_info
from lib.common.utils.globals import GlobalVar

logger = Logger("mongo_order").get_logger()


class MongoOrder:
    def __init__(self):
        server_info = GlobalVar.ZK_CLIENT_IN.get_node_info("com.oppo.zeus.mongo.order.service.QueryConsumeService")
        self.conn = DubRunner(server_info['ip_port'][0], server_info['ip_port'][1])

    def queryConsumeAmountBySsoid(self, ssoid):
        """
        根据ssoid查询消费金额
        :return:
        """
        result = self.conn.invoke(
            "com.oppo.zeus.mongo.order.service.QueryConsumeService",
            "queryComsumeAmountBySsoid",
            ssoid,
            flag="SINGLE_STRING"
        )


if __name__ == '__main__':
    MongoOrder().queryConsumeAmountBySsoid("2076075925")