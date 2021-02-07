#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/7 14:26
# comment:
import json

from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.logger.logging import Logger
from lib.common.utils.env import get_dubbo_info

logger = Logger("mongo_order").get_logger()


class MongoOrder:
    def __init__(self):
        dubbo_info = get_dubbo_info("mongo_order")
        self.conn = DubRunner(dubbo_info[0], dubbo_info[1])

    def queryConsumeAmountBySsoid(self, ssoid):
        """
        根据ssoid查询消费金额
        :return:
        """
        result = self.conn.invoke(
            "QueryConsumeService",
            "queryComsumeAmountBySsoid",
            ssoid,
            flag="SINGLE_STRING"
        )


if __name__ == '__main__':
    MongoOrder().queryConsumeAmountBySsoid("2076075925")