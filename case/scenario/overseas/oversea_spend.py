#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
import decimal
from lib.common.utils.globals import GlobarVar
from lib.common_biz.biz_db_operate import get_balance, oversea_get_coin_rate
from lib.common_biz.fiz_assert import FizAssert
from lib.interface_biz.dubbo.oversea_coin import Coin
from lib.interface_biz.dubbo.vou import Voucher
from lib.interface_biz.http.oversea_spend import Spend
from lib.config.country_currency import currency
ssoid = GlobarVar.SSOID


def kb_spend(amount, country="VN", ssoid=ssoid):
    """
    :param amount: 元  此处的amount为可币余额 payamount为当地币，需要通过rate转换
   :param country:
    :param ssoid:
    :return:
    """
    """
    1. 初始化可币余额，发放可币与优惠券
    """
    balance_before = get_balance(ssoid, country=country, in_out="oversea")
    if balance_before != round(decimal.Decimal(0), 4):
        Coin().cocoin_pay_out(ssoid, country, str(balance_before))
    Coin().cocoin_in_come(ssoid, country, amount)
    """
    2. 调用消费接口
    """
    rate = oversea_get_coin_rate(currency[country])
    order_info = Spend(amount*rate, amount*rate, country=country, currency=currency[country]).kb_spend()
    """
    3. 检查可币与优惠券消费信息是否正确
    """
    assert get_balance(ssoid, country, "oversea") == round(decimal.Decimal(0), 4)
    """
    4. 检查订单表信息是否正确(海外纯消费，未纳入订单表)
    """

    """
    5. 检查tb_payment表是否正确，疑似海外未写？
    """
    # FizAssert(in_out="oversea").assert_tb_payment(ssoid, order_info['partner_order'], int(amount * 100))
    """
    6. 检查通知表信息是否正确
    """
    FizAssert(in_out="oversea").assert_notify(order_info["partner_order"])


def kb_vou_spend(amount, price_local, couponId, discountAmount, country="VN", ssoid=ssoid):
    """
    需梳理逻辑，待定。
    :param amount:
    :param price_local:
    :param couponId:
    :param discountAmount:
    :param country:
    :param ssoid:
    :return:
    """
    # Spend(1001, 2000).kb_vou_spend(1213222, 999)
    balance_before = get_balance(ssoid, country=country, in_out="oversea")
    if balance_before != round(decimal.Decimal(0), 4):
        Coin().cocoin_pay_out(ssoid, country, str(balance_before))
    Coin().cocoin_in_come(ssoid, country, amount)
    vou_info = Voucher("oversea").grantVoucher("2031", "KB_COUPON", "DIKOU", "1000", "999", "2076075925", "VN", "VND")
    Voucher("oversea").checkVoucher(vou_info['batchId'])
    Spend(amount, price_local).kb_vou_spend(couponId, discountAmount)


if __name__ == '__main__':
    kb_spend(100)
