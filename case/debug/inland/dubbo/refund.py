#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/7 17:20
# comment:
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.env import get_dubbo_info


class Refund:
    def __init__(self):
        dubbo_info = get_dubbo_info("dispatcher")
        self.conn = DubRunner(dubbo_info[0], dubbo_info[1])

    def refund_single(self):
        """
        单个订单退款
        :return:
        """
        data = {
            "partnerOrderId": "",
            "notifyUrl": "",
            "partnerCode": "",
            "refundType": "",
            "payReqId": "KB202009071124040380445615374082",
            "refundAmount": '1'
        }
        result = self.conn.invoke(
            "IFacade",
            "simpleRefund",
            data
        )

    def refund_by_ssoid(self, ssoid):
        """
        根基ssoid进行批量退款
        :return:
        """
        pass




if __name__ == '__main__':
    Refund().refund_single()
