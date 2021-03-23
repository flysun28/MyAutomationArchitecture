#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/8 16:45
# comment:
from lib.common.algorithm.md5 import md5
from lib.common.utils.env import get_env_id
from lib.common.utils.globals import GlobalVar
from lib.common_biz.find_key import GetKey, is_get_key_from_db
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign


class Transfer:
    def __init__(self):
        pass

    def transfer(self):
        case_dict = {
            "app_id": "30223460",
            "service": "transfer-apply",
            "format": "JSON",
            "charset": "utf8",
            "sign_type": "MD5",
            "sign": "",
            "timestamp": "2020-09-01 11:25:21",
            "version": "1.0",
            "bizContent": str({
                "applyTransInfoList":
                    [
                        {
                            "partnerOrder": RandomOrder(30).business_order("ZZ"),
                            "amount": "10",
                            "payType": "alipay",
                            "ssoid": "2000071234",
                            "currency": "CNY",
                            "channelUserId": "2088112811111403",
                            "channelLogonId": "zExrNLTmVxUgeyPPlBYq7SiajwnvtySAKmStPHkfTq43aXt07Dzs",
                            # 生产
                            # "channelLogonId": "IuGqNqTvc0WFQA5A++T8LgxKS4WuY7dXeh6PJlk0lvMDwsWog9oy",
                            "realName": "cFNhCvtZ/BbX7ADbzZQmkPEl8oiBDMleIklYyI5JD6NJCg==",
                            # 生产
                            # "realName": "FXDJyPbA+ncT0CgrJj4Kl3X2oetJ9pUvxy4zOWIBnup0yg==",
                            "imei": "a0f583c94c088cb87930ba1ae060ac33",
                            "openId": "823612926301282346834921",
                            "transferDesc": "XIAOYAO1"
                        }
                        ,
                        {
                            "partnerOrder": RandomOrder(30).business_order("ZZ"),
                            "amount": "100",
                            "payType": "wxpay",
                            "ssoid": "2000071234",
                            "currency": "CNY",
                            "channelUserId": "oCg6Xt8NvRi7jGuap_5B6XdY4oYk",
                            "channelLogonId": "zExrNLTmVxUgeyPPlBYq7SiajwnvtySAKmStPHkfTq43aXt07Dzs",
                            # 生产
                            # "channelLogonId": "IuGqNqTvc0WFQA5A++T8LgxKS4WuY7dXeh6PJlk0lvMDwsWog9oy",
                            "realName": "cFNhCvtZ/BbX7ADbzZQmkPEl8oiBDMleIklYyI5JD6NJCg==",
                            # 生产
                            # "realName": "FXDJyPbA+ncT0CgrJj4Kl3X2oetJ9pUvxy4zOWIBnup0yg==",
                            "imei": "ada658256862b2da0a61d073467e612c",
                            "openId": "823612926301282346834921",
                            "transferDesc": "test2"
                        }
                    ],
                "partnerId": "30223460",
                "applicant": "80264408",
                "notifyUrl": "http://pay.pay-test.wanyol.com/notify/receiver",
                "applyReason": "XIAOYAO"
            })
        }
        case_dict['bizContent'] = str(case_dict['bizContent'])
        temp_string = ''
        if is_get_key_from_db():
            temp_string = Sign(case_dict).join_asc_have_key() + GetKey(case_dict['app_id']).get_key_from_server_info()
        else:
            temp_string = Sign(case_dict).join_asc_have_key() + "ec25bb85a7fb426e"
        case_dict['sign'] = md5(temp_string)
        """
        # 生产地址 https://gw-opay.oppomobile.com/gateway/transfer-apply
        # 灰度地址 https://gw-opay.oppomobile.com/gateway/gray-transfer-apply
        生产环境秘钥与验证签30223460: ec25bb85a7fb426e
        """
        GlobalVar.HTTPJSON_GW_IN.post("/gateway/transfer-apply", data=case_dict)


if __name__ == '__main__':
    Transfer().transfer()
