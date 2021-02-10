#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/8 16:44
# comment:
import time

from lib.common.algorithm.md5 import md5
from lib.common.utils.globals import GlobarVar
from lib.common_biz.find_key import GetKey
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign


class OrderQuery:
    def __init__(self):
        pass

    def query_order_theme_shop(self):
        case_data = {
            "appKey": "2031",
            "nonce": RandomOrder(32).random_num(),
            # 商户订单号
            "partnerOrder": "160282944860620760968742434",
            "sign": "",
            # 时间戳
            "timestamp": int(time.time())
        }
        temp_string = Sign(case_data).join_asc_have_key("&key=") + GetKey(case_data['appKey']).get_key_from_t_key()
        case_data['sign'] = md5(temp_string, to_upper=False)
        GlobarVar.HTTPJSON_GW_IN.post("/api/pay/v1/query/order-info", data=case_data)


if __name__ == '__main__':
    OrderQuery().query_order_theme_shop()