#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
import decimal
import random
import time
from case.scenario.common_req import RECHARGE_SPEND_PAY, VOU_INLAND
from lib.common.logger.logging import Logger
from lib.common_biz.biz_db_operate import get_balance
from lib.common_biz.choose_scarlett import choose_scarlett
from lib.common_biz.fiz_assert import FizAssert
from lib.interface_biz.dubbo.near_me import Nearme
from lib.interface_biz.dubbo.vou import Voucher
from lib.interface_biz.http.query_result import queryResult
from lib.interface_biz.http.simplepay import SimplePay

logger = Logger('recharge_spend').get_logger()
req = RECHARGE_SPEND_PAY
req_vou = VOU_INLAND


def rs_only_rmb(amount, notify_amount):
    """
    商品金额==支付金额
    :return:
    """
    """
        【1】. 查询可币初始化余额, 并消费可币余额至0
    """
    balance_before = get_balance(req.ssoid)
    if balance_before != round(decimal.Decimal(0), 4):
        Nearme().nearme_add_subtract(str(balance_before), req.ssoid, 1)
        balance_before = round(decimal.Decimal(0), 4)
    """
        【2】. 调用下单接口，构造渠道回调报文
    """
    order_info = SimplePay(req.pay_channel, amount / 100, req.partner_id, req.app_version, req.interface_version,
                           req.version_exp, req.notify_url).recharge_spend_amount_is_price(amount)
    choose_scarlett(notify_amount, req.pay_channel, order_info['pay_req_id'])
    """
        【3】.调用查询结果接口
    """
    assert str(queryResult(order_info['pay_req_id'])) == "2002"
    """
        【4】. 检查可币余额是否正确
    """
    balance_after = get_balance(req.ssoid)
    try:
        assert balance_before == balance_after
        logger.info("可币余额正常")
    except AssertionError as e:
        logger.info("可币余额异常")
        raise e
    """
        【5】.检查订单表记录是否正确
    """
    FizAssert().assert_order_info(req.ssoid, order_info['pay_req_id'], amount, amount, vou_id="0")
    """
        【6】. 检查trade order表记录是否正确
    """
    FizAssert().assert_trade_order(req.ssoid, order_info['pay_req_id'], amount, amount)
    """
        【7】. 检查tb_recharge表记录是否正确(无记录)
    """
    FizAssert().assert_tb_recharge(req.ssoid, order_info['pay_req_id'], amount, flag=False)
    """
        【8】. 检查tb_payments表记录是否正确(无记录)
    """
    FizAssert().assert_tb_payment(req.ssoid, order_info['partner_order'], amount, flag=False)
    """
        【9】. 检查通知表信息是否正确
    """
    FizAssert().assert_notify(order_info["partner_order"])


def rs_with_kb_rmb(amount, notify_amount, kb_amount=round(random.uniform(0.01, 0.99), 2),
                   vou_amount=round(random.uniform(0.01, 10), 2)):
    """
    商品金额=可币余额+优惠券抵扣+人民币支付
    :param notify_amount:
    :param pay_type:
    :param kb_amount: 元
    :param vou_amount: 元  0.01-0.09两位小数
    :param partner_id:
    :param amount: 分 渠道支付金额
    :return:
    """
    """
        【1】. 查询可币初始化余额, 发放可币与优惠券
    """

    balance_before = get_balance(req.ssoid)
    if balance_before != round(decimal.Decimal(0), 4):
        Nearme().nearme_add_subtract(str(balance_before), req.ssoid, 1)
    Nearme().nearme_add_subtract(str(kb_amount), req.ssoid, 0)
    vou_info = Voucher().grantVoucher(req_vou.partner_id, req_vou.couponType, req_vou.couponDiscountType,
                                      vou_amount + 0.01, str(vou_amount), req.ssoid)
    Voucher().checkVoucher(vou_info['batchId'])
    """
        【2】. 调用下单接口，构造渠道回调报文
    """
    # 商品金额
    price = int(amount + vou_amount * 100 + kb_amount * 100)
    order_info = SimplePay(req.pay_channel, str(amount / 100), req.partner_id, req.app_version, req.interface_version,
                           req.version_exp, req.notify_url).recharge_spend_kb_and_voucher(price, vou_info['vouId'],
                                                                                             req_vou.vouType,
                                                                                             int(vou_amount * 100))
    choose_scarlett(notify_amount, req.pay_channel, order_info['pay_req_id'])
    """
        【3】.调用查询结果接口
    """
    assert str(queryResult(order_info['pay_req_id'])) == "2002" or "2001"
    """
        【4】. 检查可币余额是否正确
    """
    time.sleep(2)
    assert get_balance(req.ssoid) == round(decimal.Decimal(0), 4)
    """
        【5】.检查订单表记录是否正确
    """
    FizAssert().assert_order_info(req.ssoid, order_info['pay_req_id'], amount, price, kb_spent=int(kb_amount * 100),
                                  vou_amount=int(vou_amount * 100), vou_id=str(vou_info["vouId"]))
    """
        【6】. 检查trade order表记录是否正确
    """
    FizAssert().assert_trade_order(req.ssoid, order_info['pay_req_id'], amount, price, kb_amount=int(kb_amount * 100),
                                   vou_amount=int(vou_amount * 100))
    """
        【7】. 检查tb_recharge表记录是否正确
    """
    FizAssert().assert_tb_recharge(req.ssoid, order_info['pay_req_id'], amount, flag=False)
    """
        【8】. 检查tb_payments表记录是否正确
    """
    FizAssert().assert_tb_payment(req.ssoid, order_info['partner_order'], int(kb_amount * 100))
    """
        【9】. 检查通知表信息是否正确
    """
    FizAssert().assert_notify(order_info["partner_order"])
    """
        【10】. 检查优惠券状态是否正确
    """
    FizAssert().assert_voucher(req.ssoid, vou_info['vouId'])


if __name__ == '__main__':
    a = rs_only_rmb(1, 1)
    #rs_with_kb_rmb(1, 1)
