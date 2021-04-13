#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/18 17:38
# comment:
from lib.common.algorithm.rsa import rsa
from lib.common.file_operation.config_operation import Config
from lib.common.session.http.protobuf import ProtoBuf
from lib.common.utils.globals import HTTPJSON_IN, GlobalVar
from lib.common.utils.meta import WithLogger
from lib.common_biz.file_path import key_path
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import expend_pay_sign_string
from lib.interface_biz.http.pay_pass import Pass
from lib.pb_src.python_native import ExpendPayPb_pb2
import time

token = GlobalVar.TOKEN
key = Config(key_path).read_config("expend_pay", "key_2031")


class ExpendPay(metaclass=WithLogger):
    def __init__(self, price, partner_id, version, sdkVer, notify_url):
        self.version = version
        self.sdkVer = sdkVer
        # 分 指商品价格
        self.price = price
        self.partner_id = partner_id
        self.notify_url = notify_url

    def only_kb_spend(self):
        """
        纯可币支付
        :return:
        """
        tp_rv = Pass().pass_recharge_spend()
        r_v = tp_rv[0]
        t_p = tp_rv[1]
        req = {
            "header": {
                "version": self.version,
                "t_p": t_p,
                "imei": "",
                "model": "PCRM00",
                "apntype": "1",
                "package": "com.example.pay_demo",
                "r_v": r_v,
                "ext": "",
                "sdkVer": self.sdkVer,
                "country": "CN",
                "currency": "CNY",
                "openId": "42E1F48352C04B80910A7BBB7FDDE8022d5334806a8d9b083e64c9324c08c040",
                "brandType": "OPPO",
                "mobileos": "17",
                "androidVersion": "29"
            },
            "price": self.price,
            "count": 1,
            "productname": "ONLY_KB_SPEND",
            "productdesc": "ONLY_KB_SPEND",
            "partnerid": self.partner_id,
            "callBackUrl": self.notify_url,
            "partnerOrder": RandomOrder(32).random_string(),
            "channelId": "",
            "ver": "1.1.0",
            "source": "PaySDK",
            "attach": "",
            "sign": "",
            "order": RandomOrder(13).random_num(),
            "ip": "120.197.152.211",
            "factor": ""
        }
        string_expend_pay = expend_pay_sign_string(token, req['header']['package'], req['partnerid'],
                                                   req['partnerOrder'], req['productname'], req['productdesc'],
                                                   req['price'], req['count'])
        req['sign'] = rsa(string_expend_pay, key)
        response = ProtoBuf(ExpendPayPb_pb2).runner(HTTPJSON_IN.prefix + '/plugin/post/expendpay', 'request', req,
                                                    flag=0)
        result = ProtoBuf(ExpendPayPb_pb2).parser('Result', response)
        return result

    def kb_voucher_spend(self, vouId, vouType, vouCount):
        """
        支持场景：
            1. 纯优惠券支付，仅限消费券或红包券
            2. 优惠券+可币支付 price = 可币扣除+vouCount
        :param vouId: int
        :param vouType: int
        :param vouCount: int 分
        :return:
        """
        tp_rv = Pass().pass_recharge_spend()
        r_v = tp_rv[0]
        t_p = tp_rv[1]
        req = {
            "header": {
                "version": self.version,
                "t_p": t_p,
                "imei": "",
                "model": "PCRM00",
                "apntype": "1",
                "package": "com.example.pay_demo",
                "r_v": r_v,
                "ext": "",
                "sdkVer": self.sdkVer,
                "country": "CN",
                "currency": "CNY",
                "openId": "42E1F48352C04B80910A7BBB7FDDE8022d5334806a8d9b083e64c9324c08c040",
                "brandType": "OPPO",
                "mobileos": "17",
                "androidVersion": "29"
            },
            "price": self.price,
            "count": 1,
            "productname": "KB_AND_VOU_SPEND",
            "productdesc": "KB_AND_VOU_SPEND",
            "partnerid": self.partner_id,
            "callBackUrl": self.notify_url,
            "partnerOrder": RandomOrder(32).random_string(),
            "channelId": "",
            "ver": "1.1.0",
            "source": "PaySDK",
            "attach": "",
            "sign": "",
            "appKey": "1234",
            "voucherId": vouId,
            "voucherType": vouType,
            # 优惠券金额，单位：分
            "voucherCount": vouCount,
            "order": RandomOrder(13).random_num(),
            "ip": "120.197.152.211",
            "factor": "",
            "screenInfo": "FULL"
        }
        string_expend_pay = expend_pay_sign_string(token, req['header']['package'], req['partnerid'],
                                                   req['partnerOrder'], req['productname'], req['productdesc'],
                                                   req['price'], req['count'])
        req['sign'] = rsa(string_expend_pay, key)
        response = ProtoBuf(ExpendPayPb_pb2).runner(HTTPJSON_IN.prefix + '/plugin/post/expendpay', 'request', req,
                                                    flag=0)
        start = time.perf_counter()
        while time.perf_counter() - start < 5:
            result = ProtoBuf(ExpendPayPb_pb2).parser('Result', response)
            if str(result.baseresult.code) in ('2002', '0000'):
                break
            else:
                time.sleep(0.5)
        else:
            raise TimeoutError('%s not in [2002, 0000], exceed 5s!' %result.baseresult.code)
        return {"code": result.baseresult.code, "partner_order": req['partnerOrder']}


if __name__ == '__main__':
    ExpendPay(1).only_kb_spend()
    # ExpendPay(2).kb_voucher_spend(0, 1, 1)
