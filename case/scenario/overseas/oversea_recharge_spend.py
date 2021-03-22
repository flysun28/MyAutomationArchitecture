#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
import decimal
from case.scenario.common_req import OVERSEA_RECHARGE_SPEND, VOU_OVERSEA
from lib.common.utils.globals import GlobarVar
from lib.common_biz.biz_db_operate import get_balance, oversea_get_coin_rate
from lib.common_biz.choose_scarlett import choose_scarlett
from lib.common_biz.fiz_assert import FizAssert, is_assert
from lib.config.country_currency import currency, rate_coin
from lib.interface_biz.dubbo.oversea_coin import Coin
from lib.interface_biz.dubbo.vou import Voucher
from lib.interface_biz.http.oversea_grant_voucher import oversea_grant_voucher
from lib.interface_biz.http.oversea_query_account import oversea_query_account
from lib.interface_biz.http.oversea_recharge_spend import RechargeSpend
from lib.interface_biz.http.query_voucher import query_vou_by_id
from lib.interface_biz.scarlett.oversea_upay import upay_pay_scarlet

req = OVERSEA_RECHARGE_SPEND
req_vou = VOU_OVERSEA


def rs_only_channel(amount, notify_amount):
    """
        渠道下单金额=商品金额，点卡与短代可能存在 渠道下单金额!=商品金额
    :param amount: 元
    :param notify_amount: 元
    :return:
    """
    """
    【1】. 查询可币初始化余额
    """
    balance_before = oversea_query_account(req.country, GlobarVar.SSOID, req.partner_id)
    """
    【2】. 调用可币充值消费接口，构造渠道回调报文
    """
    order_info = RechargeSpend(amount, amount, country=req.country, currency=req.currency, pay_type=req.pay_channel,
                               version=req.interface_version,
                               partner_id=req.partner_id).recharge_spend_price_is_amount()
    choose_scarlett(notify_amount, req.pay_channel, order_info['pay_req_id'])
    """
    【3】. 检查可币余额是否正确
     """
    balance_after = oversea_query_account(req.country, GlobarVar.SSOID, req.partner_id)
    # 渠道下单金额!=商品金额 少的扣可币，多的充可币
    assert balance_after == round(decimal.Decimal((notify_amount-amount)/rate_coin[req.currency]), 4) + balance_before
    if is_assert():
        """
        【6】. 检查通知表信息是否正确
         """
        FizAssert(in_out="oversea").assert_notify(order_info["partner_order"])


def rd_with_vou_channel(amount, notify_amount):
    """
    目前只考虑notify_amount = amount
    :param amount:元
    :param notify_amount:元
    :return:
    """
    """
    1. 查询可币余额，发券
    """
    balance_before = oversea_query_account(req.country, GlobarVar.SSOID, req.partner_id)
    vou_id = oversea_grant_voucher(req_vou.vouAmount, req_vou.vouType, req_vou.country, req_vou.partner_id)
    """
    【2】. 调用充值消费即可，构造渠道回调报文
    """
    order_info = RechargeSpend(amount, notify_amount + req_vou.vouAmount, country=req.country, currency=req.currency, pay_type=req.pay_channel,
                               version=req.interface_version,
                               partner_id=req.partner_id).recharge_spend_with_voucher(str(vou_id),
                                                                                      str(req_vou.vouAmount))
    choose_scarlett(notify_amount, req.pay_channel, order_info['pay_req_id'])
    """
    【3】. 检查可币与优惠券消费信息是否正确
     """
    balance_after = oversea_query_account(req.country, GlobarVar.SSOID, req.partner_id)
    assert balance_after == round(decimal.Decimal((notify_amount-amount)/rate_coin[req.currency]), 4) + balance_before
    assert query_vou_by_id(vou_id, req.ssoid, "oversea") == "USED"
    if is_assert():
        """
        【4】. 检查通知表信息是否正确
        """
        FizAssert(in_out="oversea").assert_notify(order_info["partner_order"])
        """
        【5】.检查订单表记录是否正确
        """
        FizAssert(in_out="oversea").assert_order_info(req.ssoid, order_info['pay_req_id'], notify_amount*100,
                                                      (notify_amount + req_vou.vouAmount)*100,
                                                      kb_spent=notify_amount/rate_coin[req.currency]*100,
                                                      vou_amount=req_vou.vouAmount*100)


if __name__ == '__main__':
    #rs_only_channel(10000, 8000)
    rd_with_vou_channel(10000, 10000)

