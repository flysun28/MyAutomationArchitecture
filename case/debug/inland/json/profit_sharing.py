#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/4/9 19:33
# comment:
import time
from lib.common.algorithm.md5 import md5
from lib.common.utils.globals import GlobalVar
from lib.common_biz.find_key import GetKey
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign


def profit_sharding():
    req = {
        "appKey": "9809089",
        "nonce": RandomOrder(32).random_string(),
        # 业务线
        "partnerCode": "7272431304",
        # 商户订单号
        "partnerOrder": "12de50e89eca4ab8be203977e5df4bfa",
        "partnerProfitSharingId": RandomOrder(32).random_string(),
        # 支付订单号
        "payReqId": "",
        "receivers": "{\"amount\":\"1\",\"remark\":\"用户分账\"}",
        "sign": "",
        "timestamp": str(int(time.time() * 10 ** 3))
    }
    if req['sign'] == "":
        req['sign'] = md5(Sign(req).join_asc_have_key("&key=") + GetKey(req['appKey']).get_key_from_t_key(), to_upper=False)
    GlobalVar.HTTPJSON_GW_IN.post("/api/profit-sharing/v1/commit", data=req)


def query_profit_sharding():
    req = {
        "appKey": "9809089",
        "nonce": RandomOrder(32).random_string(),
        "partnerCode": "2031",
        "partnerProfitSharingId": RandomOrder(32).random_string(),
        "profitSharingId": "",
        "sign": "",
        "timestamp": str(int(time.time() * 10 ** 3))
    }
    if req['sign'] == "":
        req['sign'] = md5(Sign(req).join_asc_have_key("&key=") + GetKey(req['appKey']).get_key_from_t_key(), to_upper=False)
    GlobalVar.HTTPJSON_GW_IN.post("/api/profit-sharing/v1/query", data=req)


if __name__ == '__main__':
    profit_sharding()