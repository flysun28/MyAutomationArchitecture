#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2020/12/22 19:43
# comment:
from Common.tools.log.print_log import LogInfo
from Assembly.runner.dubbo_runner import DubRunner
import json
import time
from Common.common.random_order import get_random_number

logger = LogInfo('优惠券发放').get_log()


def grantVoucher(host, bizNo, couponType, couponDiscountType, conditionAmount, cutAmount, ssoid, ratio=0, maxCutAmount='0'):
    """
    10.177.43.135
    10.177.43.137
    10.177.158.19
    :return:
    """
#     conn = DubRunner('10.177.158.19', 16002)
    conn = DubRunner(host, 16002)
    json_data = {
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
    # print(json_data)
    result = conn.invoke(
        "com.oppo.voucher.api.CouponBatchGrant",
        "batchGrant",
        json_data
    )
    result_encode = result.encode("utf-8")
    result = str(result_encode, encoding="gb18030")
    logger.info(result)
    result_json = json.loads(result)
    return result_json['data']['batchId']


if __name__ == '__main__':
    print(grantVoucher("2031", "KB_COUPON", "DIKOU", "10", "6.66", "2086653073"))
