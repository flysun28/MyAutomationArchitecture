#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/7 16:18
# comment:
import json
import time
from lib.common.logger.logging import Logger
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.env import get_dubbo_info, set_global_env_id
from lib.common.utils.globals import GlobalVar

logger = Logger("voucher").get_logger()


class VoucherInland:
    def __init__(self):
        server_info = GlobalVar.ZK_CLIENT_IN.get_node_info("com.oppo.voucher.api.CouponBatchGrant")
        self.conn = DubRunner(server_info['ip_port'][0], server_info['ip_port'][1])

    def grantVoucher(self, bizNo, couponType, couponDiscountType, conditionAmount, cutAmount, ssoid, ratio=0,
                     maxCutAmount='0', count=1):
        """
        优惠券申请
        :param bizNo:
        :param couponType:
        :param couponDiscountType:
        :param conditionAmount:
        :param cutAmount:
        :param ssoid:
        :param ratio:
        :param maxCutAmount:
        :return:
        """
        data = {
            "couponName": "anto_grant" + str(int(round(time.time() * 1000))),
            "useableFromTime": "2020-01-01 00:00:00",
            "useableEndTime": "2022-12-31 00:00:00",
            "settleType": "1",
            # "2031"
            "bizNo": bizNo,
            "scopeId": "7104f7bc23e445daba913a5a96a264ac",
            "blackScopeId": "",
            "subScopeId": "",
            # "KB_COUPON"
            "couponType": couponType,
            # "DIKOU"
            "couponDiscountType": couponDiscountType,
            # 满（折扣券/消费折扣券最低消费金额）
            "conditionAmount": conditionAmount,
            # 减
            "cutAmount": cutAmount,
            # 折扣券打折
            "ratio": ratio,
            # 折扣券高低消费金额
            "maxCutAmount": maxCutAmount,
            "applyCount": count,
            "ssoidList": [ssoid],
            "batchId": ""
        }
        result = self.conn.invoke(
            "com.oppo.voucher.api.CouponBatchGrant",
            "batchGrant",
            data
        )
        return {"batchId": result['data']['batchId'], "vouId": result['data']['batchVouCreateResList'][0]['vouId']}

    def checkVoucher(self, couponBatchId):
        """
        优惠券审核
        :return:
        """
        data = {"couponBatchId": couponBatchId, "batchOperateType": "PASS"}
        result = self.conn.invoke(
            "com.oppo.voucher.api.admin.CouponBatchInfoAdmin",
            "operate",
            data
        )

    def CouponExchange(self):
        """
        :return:
        """
        data = {
            "appPackage": "com.example.pay_demo",
            "bizNo": "5456925",
            "couponCode": "62640426",
            "cutAmount": 9.99,
            "expendInfo": "{\"amount\":\"9.99\",\"vouId\":62640426}",
            "factor": "",
            "imei": "000000000000000",
            "orderAmount": 10.0,
            "requestId": "GC202104221720594800100320000",
            "ssoid": "2076075925"
        }
        result = self.conn.invoke(
            "com.oppo.voucher.api.CouponExchange",
            "couponExchange",
            data
        )


if __name__ == '__main__':
    set_global_env_id(1)
    # 满减券，满1减0.99
    vou_info = VoucherInland().grantVoucher("5456925", "KB_COUPON", "DIKOU", "0.01", "0.01", "2086100900", count=1)
    VoucherInland().checkVoucher(vou_info['batchId'])
#     # 消费券，额度10
#     vou_info = VoucherInland().grantVoucher("5456925", "KB_COUPON", "XIAOFEI", "0.01", "10", "2086100900", count=1)
#     VoucherInland().checkVoucher(vou_info['batchId'])

    flag = "2"
    if flag == "1":
        # 满减
        vou_info = VoucherInland().grantVoucher("2031", "KB_COUPON", "DIKOU", "10", "9.99", "2076075925", count=1)
        VoucherInland().checkVoucher(vou_info['batchId'])
        # 消费
    if flag == "2":
        vou_info = VoucherInland().grantVoucher("2031", "KB_COUPON", "XIAOFEI", "0", "10", "2076075925", count=1)
        VoucherInland().checkVoucher(vou_info['batchId'])



