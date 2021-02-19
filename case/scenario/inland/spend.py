#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
import random

from lib.common.utils.globals import GlobarVar
from lib.common_biz.fiz_assert import FizAssert, get_pay_req_by_partner
from lib.interface_biz.dubbo.near_me import Nearme
from lib.interface_biz.dubbo.vou import VoucherInland
from lib.interface_biz.http.expend_pay import ExpendPay
ssoid = GlobarVar.SSOID


def spend(amount=random.randint(100, 1000), ssoid=ssoid, partner_id="2031"):
    """

    :param amount: 分
    :param ssoid:
    :param partner_id:
    :return:
    """
    """
        【1】. 发放可币与优惠券
    """
    Nearme().nearme_add_subtract(str(amount/100), ssoid, 0)
    vou_info = VoucherInland().grantVoucher(partner_id, "KB_COUPON", "DIKOU", "1", "0.99", ssoid)
    VoucherInland().checkVoucher(vou_info['batchId'])
    """
        【2】. 查询当前可币余额以及优惠券信息
    """

    """
        【3】. 调用纯消费接口
    """
    result = ExpendPay(int(amount+0.99*100)).kb_voucher_spend(vou_info['vouId'], 2, 99)
    assert result['code'] == "0000"
    """
        【4】. 检查可币与优惠券消费信息是否正确
    """

    """
        【5】. 检查order_info表信息是否正确
    """
    pay_req_id = get_pay_req_by_partner(ssoid, result['partnerOrder'])
    FizAssert().assert_order_info(ssoid, pay_req_id, 0, int(amount + 0.99 * 100), amount, 99, str(vou_info["vouId"]))
    """
        【6】. 检查trade_order表信息是否正确
    """
    FizAssert().assert_trade_order(ssoid, pay_req_id, 0, int(amount + 0.99 * 100), amount, 99)
    """
        【7】. 检查通知表信息是否正确
    """


if __name__ == '__main__':
    spend()