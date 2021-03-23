#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
import random
from case.scenario.common_req import EXPEND_PAY, VOU_INLAND
from case.scenario.inland.recharge import recharge
from lib.common.utils.globals import GlobalVar
from lib.common_biz.biz_db_operate import get_pay_req_by_partner
from lib.common_biz.fiz_assert import FizAssert, is_assert
from lib.interface_biz.http.expend_pay import ExpendPay
from lib.interface_biz.http.gateway_query_account import query_account
from lib.interface_biz.http.grant_voucher import grant_voucher

req = EXPEND_PAY
req_vou = VOU_INLAND


def spend_with_kb_vou(amount):
    """
    优惠券信息在VOU类中写死消费券1分钱
    :param amount: 分
    :return:
    """
    """
        【1】. 初始化可币余额，发放可币与优惠券
    """
    balance_before = query_account(GlobalVar.SSOID)
    if balance_before != 0:
        ExpendPay(balance_before, req.partner_id, req.interface_version,
                  req.app_version, req.notify_url).only_kb_spend()
    recharge(amount, amount)
    vou_id = int(grant_voucher(amount=req_vou.vouAmount, vou_type=req_vou.vouType, appId=req_vou.partner_id))
    """
        【2】. 查询当前可币余额以及优惠券信息
    """
    """
        【3】. 调用纯消费接口
    """
    result = ExpendPay(int(amount + int(req_vou.vouAmount)), req.partner_id, req.interface_version,
                       req.app_version, req.notify_url).kb_voucher_spend(vou_id, req_vou.vouType,
                                                                         int(req_vou.vouAmount))
    assert result['code'] == "0000"
    """
        【4】. 检查可币与优惠券消费信息是否正确
    """
    if is_assert():
        """
            【5】. 检查order_info表信息是否正确
        """
        pay_req_id = get_pay_req_by_partner(req.ssoid, result['partner_order'])
        FizAssert().assert_order_info(req.ssoid, pay_req_id, 0, int(amount + int(req_vou.vouAmount)), amount,
                                      int(req_vou.vouAmount),
                                      str(vou_id))
        """
            【6】. 检查trade_order表信息是否正确
        """
        FizAssert().assert_trade_order(req.ssoid, pay_req_id, 0, int(amount + int(req_vou.vouAmount)), amount,
                                       int(req_vou.vouAmount))
        """
            【7】. 检查通知表信息是否正确
        """
        FizAssert().assert_notify(result["partner_order"])
        """
            【8】. 检查优惠券信息
        """
        FizAssert().assert_voucher(req.ssoid, vou_id)


def spend_only_kb(amount):
    """

    :return:
    """
    """
    1. 调用可币充值接口
    """
    recharge(amount, amount)
    """
    2. 查询可币余额
    """
    balance_before = query_account(GlobalVar.SSOID)
    """
    3. 调用纯消费接口
    """
    result = ExpendPay(amount, req.partner_id, req.interface_version, req.app_version, req.notify_url).only_kb_spend()
    assert result.baseresult.code == "0000"
    """
    4. 查询消费后的可币余额
    """
    balance_after = query_account(GlobalVar.SSOID)
    assert balance_before == balance_after + amount


if __name__ == '__main__':
    #spend_with_kb_vou(1)
    spend_only_kb(1)
