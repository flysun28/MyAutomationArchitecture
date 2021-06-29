#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/12 14:38
# comment: 国内海外通用
from lib.common.algorithm.md5 import md5
from lib.common.file_operation.config_operation import Config
from lib.common.utils.globals import GlobalVar
from lib.common_biz.file_path import key_path
from lib.common_biz.find_key import is_get_key_from_db, GetKey
from lib.common_biz.sign import Sign


def query_vou_by_id(vou_id, ssoid, env="inland", app_id="2031"):
    req = {"appId": app_id,
           "voucherId": vou_id,
           "ssoId": ssoid,
           "sign": ""}
    key = ''
    if env == "inland":
        if is_get_key_from_db:
            key = GetKey(req['appId']).get_key_from_voucher()
        else:
            key = Config(key_path).as_dict('inland_t_key')["key_" + req['appId']]
        req['sign'] = md5(Sign(req).join_asc_have_key("&key=") + key)
        result = GlobalVar.HTTPJSON_IN.post("/voucher/queryById", data=req)
        return result['data']['status']
    elif env == "oversea":
        if is_get_key_from_db:
            key = GetKey(req['appId'], "oversea").get_key_from_voucher()
        else:
            key = Config(key_path).as_dict('oversea_t_key')["key_" + req['appId']]
        req['sign'] = md5(Sign(req).join_asc_have_key("&key=") + key)
        result = GlobalVar.HTTPJSON_OUT.post("/voucher/queryById", data=req)
        return result['data']['status']


if __name__ == '__main__':
    query_vou_by_id(102404209, "2076075925", "oversea")
    