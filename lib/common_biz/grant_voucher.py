#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/10 0:02
# comment:


import datetime
from lib.common.algorithm.md5 import md5
from lib.common.utils.globals import GlobarVar
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign
end_time = str((datetime.datetime.now() + datetime.timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S'))


def grant_voucher():
    req = {
        "amount": 1,
        "appId": "2031",
        "appSubName": "AUTO_TEST",
        "blackScopeId": "",
        "checkName": "TEST_ACCOUNT",
        "configId": "",
        "count": 1,
        "country": "CN",
        "currency": "CNY",
        "expireTime": end_time,
        "ext1": "",
        "ext2": "",
        "maxAmount": 1,
        "name": "AUTO_TEST",
        "partnerOrder": RandomOrder(28).business_order("AUTO"),
        "ratio": "",
        "remark": "",
        "salePrice": 0,
        "scopeId": "7104f7bc23e445daba913a5a96a264ac",
        "settleType": 1,
        "sign": "",
        "ssoid": GlobarVar.SSOID,
        "subScopeId": "",
        "timezone": "",
        "type": 2,
        "useableTime": "2021-01-01 00:00:00"
    }
    req['sign'] = md5(Sign(req).join_asc_have_key("&key=") + "8m7dlr743nre123kk439r54adf2aw3fku1")
    result = GlobarVar.HTTPJSON_IN.post("/voucher/grantSingle", data=req)
    # 返回优惠券id
    return result['vouIdList'][0]
