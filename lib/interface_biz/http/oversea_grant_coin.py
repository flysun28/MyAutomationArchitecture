#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/11 22:14
# comment: 海外发放可币
import time
from lib.common.algorithm.md5 import md5
from lib.common.file_operation.config_operation import Config
from lib.common_biz.file_path import key_path
from lib.common_biz.find_key import GetKey, is_get_key_from_db
from lib.common.utils.globals import GlobarVar
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign
from lib.config.country_currency import currency


def oversea_grant_coin(app_key, partner_id, country, ssoid, amount):
    """
    :param app_key:
    :param partner_id:
    :param country:
    :param ssoid:
    :param amount: 后端接口传分，此处转成元。即amount=1, 充值可币1元。
    :return:
    """
    case_req = {
        "appKey": app_key,
        "sign": "",
        "timestamp": int(time.time()),
        "nonce": RandomOrder(32).random_num(),
        "partnerCode": partner_id,
        "partnerOrder": RandomOrder(32).random_string(),
        "country": country,
        "currency": currency[country],
        "ssoid": ssoid,
        "amount": amount*100
    }
    key = ''
    if is_get_key_from_db:
        key = GetKey(partner_id, "oversea").get_key_from_t_key()
    else:
        key = Config(key_path).as_dict('oversea_t_key')["key_" + partner_id]
    case_req['sign'] = md5(Sign(case_req).join_asc_have_key(salt="&key=") + key, False)
    response = GlobarVar.HTTPJSON_GW_OUT.post("/api/cocoin/grant", data=case_req)


if __name__ == '__main__':
    oversea_grant_coin("2031", "2031", "VN", "2076075925", 1)
