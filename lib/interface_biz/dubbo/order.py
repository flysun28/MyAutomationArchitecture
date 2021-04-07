#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/8 14:14
# comment:
from lib.common.file_operation.config_operation import Config
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.env import get_dubbo_info
from lib.common.utils.globals import GlobalVar
from lib.common_biz.order_random import RandomOrder
from lib.config.path import common_sql_path


class Order:
    
    def __init__(self):
        server_info = GlobalVar.ZK_CLIENT_IN.get_node_info("com.oppo.pay.order.facade.RefundLogic")
        self.conn = DubRunner(server_info['ip_port'][0], server_info['ip_port'][1])

    def refund_approval(self, partnerId, partnerOrder, refundAmount, payType, payReqId=""):
        """
        退款审批
        :return:
        """

        data_temp_1 = {"fileUrl": "",
                       "applyAccount": "80264408",
                       "batchNo": RandomOrder(32).random_num(),
                       "partnerId": partnerId,
                       "approveType": "CASH",
                       "class": "com.oppo.pay.order.facade.dto.BatchRefundCommonInfo"}
        data_temp_2 = [{"partnerOrder": partnerOrder,
                        "notifyUrl": "wwww.baidu.com",
                        "payReqId": payReqId,
                        "refundAmount": refundAmount,
                        "refundReason": "AUTO_TEST",
                        "payType": payType,
                        "class": "com.oppo.pay.order.facade.dto.BatchRefundRecord"}]
        data = str(data_temp_1) + "," + str(data_temp_2)
        result = self.conn.invoke(
            "RefundLogic",
            "approvalRefund",
            data,
            "FIX"
        )
        mysql = GlobalVar.MYSQL_IN
        mysql.execute(str(Config(common_sql_path).read_config("refund", "refund_update")).format(payReqId))


if __name__ == '__main__':
    Order().refund_approval("5456925", "149ee2d6e62547e6bbcaf8105ae00b48", "0.01", "alipay", "KB202101251049252076075925174742")