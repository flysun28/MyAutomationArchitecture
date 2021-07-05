#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
import decimal
from case.scenario.common_req import OVERSEA_SPEND, VOU_OVERSEA
from lib.common.utils.globals import GlobalVar
from lib.common_biz.biz_db_operate import oversea_get_coin_rate
from lib.common_biz.fiz_assert import FizAssert, is_assert
from lib.interface_biz.http.oversea_grant_coin import oversea_grant_coin
from lib.interface_biz.http.oversea_grant_voucher import oversea_grant_voucher
from lib.interface_biz.http.oversea_query_account import oversea_query_account
from lib.interface_biz.http.oversea_spend import Spend
from lib.common.utils.constants import currency, rate_coin
from lib.interface_biz.http.query_voucher import query_vou_by_id

req = OVERSEA_SPEND
req_vou = VOU_OVERSEA


def kb_spend(amount):
    """
    :param amount: 元  此处的amount为可币金额 spend接口中payamount为当地币，需要通过rate转换
    :return:
    """
    """
    1. 发可币
    """
    # app_key测试环境==partner_id，生产需单独处理
    oversea_grant_coin(req.partner_id, req.partner_id, req.country, GlobalVar.SSOID, amount)
    balance_before = oversea_query_account(req.country, GlobalVar.SSOID, req.partner_id)
    """
    2. 调用消费接口
    """
    rate = rate_coin[req.currency]
    order_info = Spend(amount*rate, amount*rate, version=req.interface_version, partner_id=req.partner_id,
                       country=req.country, currency=currency[req.country]).kb_spend()
    """
    3. 检查可币与优惠券消费信息是否正确
    """
    balance_after = oversea_query_account(req.country, GlobalVar.SSOID, req.partner_id)
    assert balance_before == balance_after + round(decimal.Decimal(amount), 4)
    """
    4. 检查订单表信息是否正确(海外纯消费，未纳入订单表)
    """

    """
    5. 检查tb_payment表是否正确，疑似海外未写？
    """
    # FizAssert(in_out="oversea").assert_tb_payment(ssoid, order_info['partner_order'], int(amount * 100))
    if is_assert():
        """
        6. 检查通知表信息是否正确
        """
        FizAssert(in_out="oversea").assert_notify(order_info["partner_order"])


def kb_vou_spend(amount):
    """
            discountAmount + pay_amount = priceLocal
            接口传入的是当地币金额
            海外无消费券，此处造的消费券；海外无渠道+可币+优惠券支付
    需梳理逻辑，待定。
    :param amount: 可币支付金额
    :return:
    """
    """
    1. 发可币, 发券
    """
    # app_key测试环境==partner_id，生产需单独处理
    oversea_grant_coin(req.partner_id, req.partner_id, req.country, GlobalVar.SSOID, amount)
    balance_before = oversea_query_account(req.country, GlobalVar.SSOID, req.partner_id)

    vou_id = oversea_grant_voucher(req_vou.vouAmount, req_vou.vouType, req_vou.country, req_vou.partner_id)
    rate = float(oversea_get_coin_rate(currency[req.country]))
    """
    2. 调用消费接口
    """
    order_info = Spend(amount * rate, amount * rate + req_vou.vouAmount, version=req.interface_version, partner_id=req.partner_id,
          country=req.country, currency=currency[req.country]).kb_vou_spend(vou_id, req_vou.vouAmount)
    """
        3. 检查可币与优惠券消费信息是否正确
    """
    balance_after = oversea_query_account(req.country, GlobalVar.SSOID, req.partner_id)
    assert balance_after == balance_before - round(decimal.Decimal(amount), 4)
    assert query_vou_by_id(vou_id, req.ssoid, "oversea") == "USED"
    if is_assert():
        FizAssert(in_out="oversea").assert_voucher(req.ssoid, vou_id)
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


if __name__ == '__main__':
    # 传参是可币的金额，已经经过了换算
    #kb_spend(0.01)
    kb_vou_spend(0.01)
