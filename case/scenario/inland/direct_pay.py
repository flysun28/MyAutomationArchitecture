#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
import random
from lib.common.logger.logging import Logger
from lib.common.utils.globals import GlobarVar
from lib.common_biz.find_key import GetKey
from time import sleep
from lib.common_biz.find_merchant_info import FindMerchant
from lib.common_biz.fiz_assert import FizAssert
from lib.interface_biz.http.query_result import queryResult
from lib.interface_biz.http.simplepay import SimplePay
from lib.interface_biz.scarlett.wxpay import wx_normal_pay_scarlet


ssoid = GlobarVar.SSOID

merchant_info = FindMerchant("2031").find_app_id_merchant("wxpay")
md5_key = GetKey("").get_md5_key_from_merchant(merchant_info["app_id"], merchant_info["merchant_no"], "wxpay")
logger = Logger('direct_pay').get_logger()


def direct_pay(amount=random.randint(1, 1000)):
    """
    :param amount: 分
    :return:
    """
    """
        【1】. 调用直扣接口，构造渠道回调报文
    """
    order = SimplePay("wxpay", amount/100).direct_pay()
    sleep(1)
    wx_normal_pay_scarlet(merchant_info["merchant_no"], order["pay_req_id"], merchant_info["app_id"], amount, md5_key)
    """
        【2】. 调用查询结果接口
    """
    assert str(queryResult(order["pay_req_id"], "direct")) == "2002"
    """
        【3】. 检查order_info表信息是否正确
    """
    FizAssert().assert_order_info(ssoid, order["pay_req_id"], amount, amount)
    """
        【4】. 检查trade_order表信息是否正确
    """
    FizAssert().assert_trade_order(ssoid, order["pay_req_id"], amount, amount)
    """
        【5】. 检查通知表信息是否正确
    """
    FizAssert().assert_notify(order["partner_order"])


if __name__ == '__main__':
    direct_pay()
