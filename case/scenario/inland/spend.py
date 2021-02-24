#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
import decimal
import random
from lib.common.utils.globals import GlobarVar
from lib.common_biz.biz_db_operate import get_pay_req_by_partner, get_balance
from lib.common_biz.fiz_assert import FizAssert
from lib.interface_biz.dubbo.near_me import Nearme
from lib.interface_biz.dubbo.vou import VoucherInland
from lib.interface_biz.http.expend_pay import ExpendPay
ssoid = GlobarVar.SSOID


def spend(amount, ssoid=ssoid, partner_id="2031",
          vou_amount=round(random.uniform(0.02, 10), 2)):
    """
    满vou_amount+0.01，减vou_amount优惠券
    :param vou_amount: 元
    :param amount: 分
    :param ssoid:
    :param partner_id:
    :return:
    """
    """
        【1】. 初始化可币余额，发放可币与优惠券
    """
    balance_before = get_balance(ssoid)
    if balance_before != round(decimal.Decimal(0), 4):
        ExpendPay(int(round(float(balance_before), 4) * 100)).only_kb_spend()
    Nearme().nearme_add_subtract(amount/100, ssoid, 0)
    vou_info = VoucherInland().grantVoucher(partner_id, "KB_COUPON", "DIKOU", vou_amount+0.01, vou_amount, ssoid)
    VoucherInland().checkVoucher(vou_info['batchId'])
    """
        【2】. 查询当前可币余额以及优惠券信息
    """
    """
        【3】. 调用纯消费接口
    """
    result = ExpendPay(int(amount+vou_amount*100)).kb_voucher_spend(vou_info['vouId'], 2, int(vou_amount*100))
    assert result['code'] == "0000"
    """
        【4】. 检查可币与优惠券消费信息是否正确
    """

    """
        【5】. 检查order_info表信息是否正确
    """
    pay_req_id = get_pay_req_by_partner(ssoid, result['partner_order'])
    FizAssert().assert_order_info(ssoid, pay_req_id, 0, int(amount + vou_amount * 100), amount, int(vou_amount*100), str(vou_info["vouId"]))
    """
        【6】. 检查trade_order表信息是否正确
    """
    FizAssert().assert_trade_order(ssoid, pay_req_id, 0, int(amount + vou_amount * 100), amount, int(vou_amount*100))
    """
        【7】. 检查通知表信息是否正确
    """
    FizAssert().assert_notify(result["partner_order"])
    """
        【8】. 检查优惠券信息
    """
    FizAssert().assert_voucher(vou_info['vouId'])


if __name__ == '__main__':
    a = spend(1)



