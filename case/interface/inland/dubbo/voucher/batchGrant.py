#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/17 19:20
# comment:
from lib.common.utils.globals import GlobalVar
from lib.common_biz.replace_parameter import replace_gateway


def batchGrant():
    req = {
     'app_id': '000000',
     'service': 'batchGrant',
     'format': 'JSON',
     'charset': 'utf8',
     'sign_type': 'MD5',
     'sign': '',
     'timestamp': '',
     'version': '1.0',
     'bizContent': "{'couponName': 'anto_grant1615985546027', 'useableFromTime': '2020-01-01 00:00:00', "
                   "'useableEndTime': '2022-12-31 00:00:00', 'settleType': '1', 'bizNo': '5456925', 'scopeId': "
                   "'7104f7bc23e445daba913a5a96a264ac', 'blackScopeId': '', 'subScopeId': '', 'couponType': "
                   "'KB_COUPON', 'couponDiscountType': 'DIKOU', 'conditionAmount': '0.01', 'cutAmount': '0.01', "
                   "'ratio': 0, 'maxCutAmount': '0', 'applyCount': 1, 'ssoidList': ['2086100900'], 'batchId': ''} "
}
    replace_gateway(req, req['app_id'])
    response = GlobalVar.HTTPJSON_GW_IN.post("/gateway/batchGrant", data=req)


if __name__ == '__main__':
    batchGrant()