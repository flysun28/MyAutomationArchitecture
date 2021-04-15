#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
import decimal
import time
from case.scenario.common_req import RECHARGE_SPEND_PAY, VOU_INLAND
from case.scenario.inland.recharge import recharge
from lib.common.logger.logging import Logger
from lib.common.utils.globals import GlobalVar
from lib.common_biz.choose_scarlett import choose_scarlett
from lib.common_biz.fiz_assert import FizAssert, is_assert
from lib.interface_biz.http.expend_pay import ExpendPay
from lib.interface_biz.http.gateway_query_account import query_account
from lib.interface_biz.http.grant_voucher import grant_voucher
from lib.interface_biz.http.query_result import queryResult
from lib.interface_biz.http.simplepay import SimplePay
from lib.common.exception import WaitUntilTimeOut

logger = Logger('recharge_spend').get_logger()
req = RECHARGE_SPEND_PAY
req_vou = VOU_INLAND


def rs_only_rmb(amount, notify_amount):
    """
    商品金额==支付金额 分
    :return:
    """
    """
        【1】. 查询可币初始化余额, 并消费可币余额至0
    """
    balance_before = query_account(GlobalVar.SSOID)
    if balance_before != 0:
        ExpendPay(balance_before, req.partner_id, req.interface_version,
                  req.app_version, req.notify_url).only_kb_spend()
        balance_before = query_account(GlobalVar.SSOID)
    """
        【2】. 调用下单接口，构造渠道回调报文
    """
    order_info = SimplePay(req.pay_channel, amount, req.partner_id, req.app_version, req.interface_version,
                           req.version_exp, req.notify_url).recharge_spend_amount_is_price(amount)
    choose_scarlett(notify_amount, req.pay_channel, order_info['pay_req_id'], partner_id=req.partner_id)
    """
        【3】.调用查询结果接口
    """
    start = time.perf_counter()
    while time.perf_counter() - start < 5:
        try:
            query_res = queryResult(order_info["pay_req_id"])
            assert query_res == '2002', '%s != 2002' %query_res
        except AssertionError as e:
            time.sleep(0.5)
        else:
            break
    else:
        raise TimeoutError('%s, exceed 5s!' %e)
    """
        【4】. 检查可币余额是否正确
    """
    balance_after = query_account(GlobalVar.SSOID)
    try:
        assert balance_before == balance_after
        logger.info("可币余额正常")
    except AssertionError as e:
        logger.info("可币余额异常")
        raise e
    """
        【5】.检查订单表记录是否正确
    """
    if is_assert():
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
        FizAssert().assert_notify(order_info["partner_order"], amount)


def rs_with_kb_rmb(amount, notify_amount, kb_amount):
    """
    商品金额=可币余额+优惠券抵扣+人民币支付(优惠券金额写死在VOU类中)
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

    balance_before = query_account(GlobalVar.SSOID)
    if balance_before != 0:
        ExpendPay(balance_before, req.partner_id, req.interface_version,
                  req.app_version, req.notify_url).only_kb_spend()
    recharge(amount, amount)
    vou_id = int(grant_voucher(amount=req_vou.vouAmount, vou_type=req_vou.vouType, appId=req_vou.partner_id))
    """
        【2】. 调用下单接口，构造渠道回调报文
    """
    # 商品金额
    price = int(amount + int(req_vou.vouAmount) + kb_amount)
    order_info = SimplePay(req.pay_channel, amount, req.partner_id, req.app_version, req.interface_version,
                           req.version_exp, req.notify_url).recharge_spend_kb_and_voucher(price, vou_id,
                                                                                          req_vou.vouType,
                                                                                          int(req_vou.vouAmount))
    choose_scarlett(notify_amount, req.pay_channel, order_info['pay_req_id'], partner_id=req.partner_id)
    """
        【3】.调用查询结果接口
    """
    assert str(queryResult(order_info['pay_req_id'])) == "2002" or "2001"
    """
        【4】. 检查可币余额是否正确
    """
    time.sleep(2)
    balance = query_account(GlobalVar.SSOID)
    assert balance == round(decimal.Decimal(0), 4), (balance, round(decimal.Decimal(0), 4))
    """
        【5】.检查订单表记录是否正确
    """
    FizAssert().assert_order_info(req.ssoid, order_info['pay_req_id'], amount, price, kb_spent=int(kb_amount),
                                  vou_amount=int(req_vou.vouAmount), vou_id=str(vou_id))
    """
        【6】. 检查trade order表记录是否正确
    """
    FizAssert().assert_trade_order(req.ssoid, order_info['pay_req_id'], amount, price, kb_amount=int(kb_amount),
                                   vou_amount=int(req_vou.vouAmount))
    """
        【7】. 检查tb_recharge表记录是否正确
    """
    FizAssert().assert_tb_recharge(req.ssoid, order_info['pay_req_id'], amount, flag=False)
    """
        【8】. 检查tb_payments表记录是否正确
    """
    FizAssert().assert_tb_payment(req.ssoid, order_info['partner_order'], int(kb_amount))
    """
        【9】. 检查通知表信息是否正确
    """
    FizAssert().assert_notify(order_info["partner_order"], price)
    """
        【10】. 检查优惠券状态是否正确
    """
    FizAssert().assert_voucher(req.ssoid, vou_id)


if __name__ == '__main__':
#     rs_only_rmb(1, 1)
    rs_with_kb_rmb(1, 1, 1)
