#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/9 23:42
# comment: 单张优惠券申请
import datetime
from lib.common.algorithm.md5 import md5
from lib.common.file_operation.config_operation import Config
from lib.common.utils.globals import GlobalVar
from lib.common_biz.file_path import key_path
from lib.common_biz.find_key import is_get_key_from_db, GetKey
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign
end_time = str((datetime.datetime.now() + datetime.timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S'))


def grant_voucher(amount=1, vou_type=1, appId="2031"):
    """
    默认消费券
    :param appId: 
    :param vou_type: 
    :param amount: 分
    :return:
    """
    req = {
        "amount": amount,
        "appId": appId,
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
        "ssoid": GlobalVar.SSOID,
        "subScopeId": "",
        "timezone": "",
        # 1 消费券
        "type": vou_type,
        "useableTime": "2021-01-01 00:00:00"
    }
    key = ''
    if is_get_key_from_db:
        key = GetKey(req['appId']).get_key_from_voucher()
    else:
        key = Config(key_path).as_dict('oversea_vou_app_info')["key_" + req['appId']]
    req['sign'] = md5(Sign(req).join_asc_have_key("&key=") + key)
    result = GlobalVar.HTTPJSON_IN.post("/voucher/grantSingle", data=req)
    # 返回优惠券id
    return result['vouIdList'][0]


if __name__ == '__main__':
   print(grant_voucher())
