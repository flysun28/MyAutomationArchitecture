#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
import random

from lib.common.logger.logging import Logger
from lib.common.utils.globals import GlobarVar
from lib.common_biz.biz_db_operate import get_balance
from lib.common_biz.find_key import GetKey
from lib.common_biz.find_merchant_info import FindMerchant
from lib.common_biz.fiz_assert import FizAssert
from lib.interface_biz.http.query_result import queryResult
from lib.interface_biz.http.simplepay import SimplePay
from lib.interface_biz.scarlett.wxpay import wx_normal_pay_scarlet

ssoid = GlobarVar.SSOID
merchant_info = FindMerchant("2031").find_app_id_merchant("wxpay")
md5_key = GetKey("").get_md5_key_from_merchant(merchant_info["app_id"], merchant_info["merchant_no"], "wxpay")
logger = Logger('recharge_spend').get_logger()


def rs_only_rmb(amount=random.randint(1, 1000)):
    """
    商品金额==支付金额
    :return:
    """
    """
        【1】. 查询可币初始化余额
    """
    balance_before = get_balance(ssoid)

    """
        【2】. 调用下单接口接口，构造渠道回调报文
    """
    order_info = SimplePay("wxpay", str(amount/100)).recharge_spend_amount_is_price(amount)
    wx_normal_pay_scarlet(merchant_info["merchant_no"], order_info["pay_req_id"], merchant_info["app_id"], amount, md5_key)

    """
        【3】.调用查询结果接口
    """
    assert str(queryResult(order_info['pay_req_id'])) == "2002"
    """
        【4】. 检查可币余额是否正确
    """
    balance_after = get_balance(ssoid)
    try:
        assert balance_before == balance_after
        logger.info("可币余额正常")
    except AssertionError as e:
        logger.info("可币余额异常")
        raise e
    """
        【5】.检查订单表记录是否正确
    """
    FizAssert().assert_order_info(ssoid, order_info['pay_req_id'], amount, amount, vou_id="0")
    """
        【6】. 检查trade order表记录是否正确
    """
    FizAssert().assert_trade_order(ssoid, order_info['pay_req_id'], amount, amount)
    """
        【7】. 检查tb_recharge表记录是否正确(无记录)
    """
    FizAssert().assert_tb_recharge(ssoid, order_info['pay_req_id'], amount, flag=False)
    """
        【8】. 检查tb_payments表记录是否正确(无记录)
    """
    FizAssert().assert_tb_payment(ssoid, order_info['partner_order'], amount, flag=False)


if __name__ == '__main__':
    rs_only_rmb()
