#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/11 20:43
# comment: 海外查询可币余额
import decimal
from lib.common.algorithm.md5 import md5
from lib.common.file_operation.config_operation import Config
from lib.common_biz.file_path import key_path
from lib.common_biz.find_key import GetKey, is_get_key_from_db
from lib.common.utils.globals import GlobarVar
from lib.common_biz.sign import Sign


def oversea_query_account(country, ssoid, partner_id):
    """
    :return:
    """
    case_req = {"country": country,
                "partnerId": partner_id,
                "sign": "",
                "ssoid": ssoid,
                "version": "1.0"}
    key = ''
    if is_get_key_from_db:
        key = GetKey(partner_id, "oversea").get_key_from_merchant()
    else:
        key = Config(key_path).as_dict('oversea_merchant')["key_" + partner_id]
    case_req['sign'] = md5(Sign(case_req).join_asc_have_key(salt="&key=") + key, False)
    response = GlobarVar.HTTPJSON_OUT.post("/plugin/post/queryCocoinBalance", data=case_req)
    return round(decimal.Decimal(response['balance']), 4)


if __name__ == '__main__':
    oversea_query_account("IN", GlobarVar.SSOID, "2031")