#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
import decimal
from case.scenario.common_req import OVERSEA_RECHARGE_SPEND, VOU_OVERSEA
from lib.common_biz.biz_db_operate import get_balance, oversea_get_coin_rate
from lib.common_biz.fiz_assert import FizAssert
from lib.config.country_currency import currency
from lib.interface_biz.dubbo.oversea_coin import Coin
from lib.interface_biz.dubbo.vou import Voucher
from lib.interface_biz.http.oversea_recharge_spend import RechargeSpend
from lib.interface_biz.scarlett.oversea_upay import upay_pay_scarlet

req = OVERSEA_RECHARGE_SPEND
req_vou = VOU_OVERSEA


def rs_only_rmb(amount, notify_amount):
    """
        渠道下单金额=商品金额，点卡与短代可能存在 渠道下单金额!=商品金额
    :param amount: 元
    :param notify_amount: 分
    :return:
    """
    """
    【1】. 查询可币初始化余额, 并置为0
    """
    balance_before = get_balance(req.ssoid, country=req.country, in_out="oversea")
    Coin().cocoin_pay_out(req.ssoid, req.country, str(balance_before))
    """
    【2】. 调用可币充值接口，构造渠道回调报文
    """
    order_info = RechargeSpend(amount, amount, country=req.country, currency=req.currency, pay_type=req.pay_channel,
                               version=req.interface_version,
                               partner_id=req.partner_id).recharge_spend_price_is_amount()
    upay_pay_scarlet(notify_amount, order_info['pay_req_id'])
    """
    【3】. 检查可币与优惠券消费信息是否正确
     """
    assert get_balance(req.ssoid, req.country, "oversea") == round(decimal.Decimal(0), 4)
    """
    【6】. 检查通知表信息是否正确
    """
    FizAssert(in_out="oversea").assert_notify(order_info["partner_order"])


def rd_with_vou_rmb(amount, notify_amount, discountAmount):
    """
    :param discountAmount:
    :param amount:
    :param notify_amount:
    :return:
    """
    balance_before = get_balance(req.ssoid, country=req.country, in_out="oversea")
    if balance_before != round(decimal.Decimal(0), 4):
        Coin().cocoin_pay_out(req.ssoid, req.country, str(balance_before))
    vou_info = Voucher("oversea").grantVoucher(req.partner_id, req_vou.couponType, req_vou.couponDiscountType,
                                               str(discountAmount + 1000), str(discountAmount), req.ssoid, req.country,
                                               req.currency)
    Voucher("oversea").checkVoucher(vou_info['batchId'])
    """
    【2】. 调用充值消费即可，构造渠道回调报文
    """
    order_info = RechargeSpend(amount, notify_amount/100 + discountAmount, country=req.country, currency=req.currency, pay_type=req.pay_channel,
                               version=req.interface_version,
                               partner_id=req.partner_id).recharge_spend_with_voucher(str(vou_info["vouId"]),
                                                                                      str(discountAmount))
    upay_pay_scarlet(notify_amount, order_info['pay_req_id'])
    """
    【3】. 检查可币与优惠券消费信息是否正确
     """
    assert get_balance(req.ssoid, req.country, "oversea") == round(decimal.Decimal(0), 4)
    """
    【4】. 检查通知表信息是否正确
    """
    FizAssert(in_out="oversea").assert_notify(order_info["partner_order"])
    """
    【5】.检查订单表记录是否正确
    """
    rate = oversea_get_coin_rate(currency[req.country])
    FizAssert(in_out="oversea").assert_order_info(req.ssoid, order_info['pay_req_id'], notify_amount,
                                                  (notify_amount/100 + discountAmount)*100,
                                                  kb_spent=notify_amount/rate, vou_amount=discountAmount*100)


if __name__ == '__main__':
    #rs_only_rmb(10000, 1000000)
    rd_with_vou_rmb(10000, 1000000, 10000)

