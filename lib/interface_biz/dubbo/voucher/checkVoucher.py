#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2020/12/23 14:26
# comment: 优惠券审核
from Common.tools.log.print_log import LogInfo
from Assembly.runner.dubbo_runner import DubRunner
import json
logger = LogInfo('优惠券审核').get_log()


def checkVoucher(couponBatchId):
    """
    10.177.43.135
    10.177.43.137
    10.177.158.19
    :return:
    """
    conn = DubRunner('10.177.158.19', 16002)
    json_data = {"couponBatchId": couponBatchId, "batchOperateType":"PASS"}
    # print(json_data)
    result = conn.invoke(
        "com.oppo.voucher.api.admin.CouponBatchInfoAdmin",
        "operate",
        json_data
    )
    logger.info(result.encode("GBK", "ignore"))


if __name__ == '__main__':
    checkVoucher("")