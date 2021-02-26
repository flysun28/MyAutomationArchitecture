#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
import decimal
from lib.common.utils.globals import GlobarVar
from lib.common_biz.biz_db_operate import get_balance
from lib.interface_biz.dubbo.oversea_coin import Coin
from lib.interface_biz.dubbo.vou import Voucher
from lib.interface_biz.http.oversea_spend import Spend
ssoid = GlobarVar.SSOID


def kb_spend(amount, country="VN", ssoid=ssoid):
    """
    :param amount: 元
    :param country:
    :param ssoid:
    :return:
    """
    """
    1. 初始化可币余额，发放可币与优惠券
    """
    balance_before = get_balance(ssoid, country=country, in_out="oversea")
    if balance_before != round(decimal.Decimal(0), 4):
        Spend(balance_before, balance_before).kb_spend()
    Coin().cocoin_in_come(ssoid, country, amount)
    # vou_info = Voucher("oversea").grantVoucher("2031", "KB_COUPON", "DIKOU", "1000", "999", "2076075925", "VN", "VND")
    # Voucher("oversea").checkVoucher(vou_info['batchId'])
    """
    2. 调用消费接口
    """
    Spend(amount, amount).kb_spend()
    """
    3. 检查可币与优惠券消费信息是否正确
    """

    """
    4. 检查订单表信息是否正确(海外纯消费，未纳入订单表)
    """

    """
    5. 检查优惠券状态是否正确
    """

    """
    6. 检查通知表信息是否正确
    """


if __name__ == '__main__':
    kb_spend(100)