#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/19 17:08
# comment:
from lib.common.file_operation.config_operation import Config
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.env import get_dubbo_info
from lib.common.utils.globals import GlobarVar
import time

from lib.config.path import common_sql_path


class VoucherInland:
    def __init__(self, in_out="inland"):
        self.in_out = in_out
        dubbo_info = get_dubbo_info("voucher", self.in_out)
        self.conn = DubRunner(dubbo_info[0], dubbo_info[1])
        if in_out == "inland":
            self.mysql = GlobarVar.MYSQL_IN
        if in_out == "oversea":
            self.mysql_out = GlobarVar.MYSQL_OUT

    def grantVoucher(self, bizNo, couponType, couponDiscountType, conditionAmount, cutAmount, ssoid, country="",
                     currency='', ratio=0, maxCutAmount='0'):
        """
        优惠券申请
        :param currency: 海外需要传
        :param country: 海外需要传
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
        scopeId = ''
        if self.in_out == "inland":
            scopeId = self.mysql.select_one(str(Config(common_sql_path).read_config("voucher", "scope_id")).
                                            format("all"))['scopeId']
        elif self.in_out == "oversea":
            scopeId = self.mysql_out.select_one(str(Config(common_sql_path).read_config("voucher", "scope_id_oversea")).
                                                format("all"))['scopeId']
        data = {
            "couponName": "anto_grant" + str(int(round(time.time() * 1000))),
            "useableFromTime": "2020-01-01 00:00:00",
            "useableEndTime": "2022-12-31 00:00:00",
            "settleType": "1",
            # "2031"
            "bizNo": bizNo,
            "scopeId": scopeId,
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
        if self.in_out == "oversea":
            # 海外需要额外的字段
            data['country'] = country
            data['currency'] = currency
            data["timezone"] = "GMT+07:00"
            data["isAdmin"] = "true"
            data["applyUserName"] = "80264408"
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
    # 抵扣券
    # vou_info = VoucherInland().grantVoucher("2031", "KB_COUPON", "DIKOU", "10", "9.99", "2076075925")
    # VoucherInland().checkVoucher(vou_info['batchId'])

    vou_info = VoucherInland("oversea").grantVoucher("2031", "KB_COUPON", "DIKOU", "1000", "999", "2076075925", "VN", "VND")
    VoucherInland("oversea").checkVoucher(vou_info['batchId'])
    # 红包券
    # vou_info = VoucherInland().grantVoucher("5456925", "KB_COUPON", "RED_PACKET_COUPON", "0", "10", "2076075925")
    # VoucherInland().checkVoucher(vou_info['batchId'])
