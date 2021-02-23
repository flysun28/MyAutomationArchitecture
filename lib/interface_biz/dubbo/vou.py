#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/19 17:08
# comment:
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.env import get_dubbo_info
import time


class VoucherInland:
    def __init__(self):
        dubbo_info = get_dubbo_info("voucher_in")
        self.conn = DubRunner(dubbo_info[0], dubbo_info[1])

    def grantVoucher(self, bizNo, couponType, couponDiscountType, conditionAmount, cutAmount, ssoid, ratio=0,
                     maxCutAmount='0'):
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
            "applyCount": "1",
            "ssoidList": [ssoid],
            "batchId": ""
        }
        result = self.conn.invoke(
            "com.oppo.voucher.api.CouponBatchGrant",
            "batchGrant",
            data
        )
        return {"batchId": result['data']['batchId'], "vouId": int(result['data']['batchVouCreateResList'][0]['vouId'])}

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


if __name__ == '__main__':
    #vou_info = VoucherInland().grantVoucher("5456925", "KB_COUPON", "DIKOU", "10", "9.99", "2076075547")
    # 红包券
    vou_info = VoucherInland().grantVoucher("5456925", "KB_COUPON", "RED_PACKET_COUPON", "0", "10", "2076075925")
    VoucherInland().checkVoucher(vou_info['batchId'])
