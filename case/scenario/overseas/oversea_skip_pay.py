#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
from lib.common.utils.globals import GlobarVar
from lib.common_biz.fiz_assert import FizAssert
from lib.interface_biz.http.oversea_skippay import Skippay
from lib.interface_biz.scarlett.oversea_coda import coda_pay
ssoid = GlobarVar.SSOID


def skip_pay(amount, notify_amount, payType="codapay_store"):
    """
    :param amount: 元
    :param notify_amount:
    :param payType:
    :return:
    """
    """
    【1】. 调用直扣接口，构造渠道回调报文
    """
    order_info = Skippay(amount, amount, payType=payType).skip_pay()
    coda_pay(notify_amount, "390", "24", order_info['pay_req_id'])
    """
    【2】. 调用查询结果接口?疑似少部分渠道有？
    """
    """
    【3】. 检查order_info表信息是否正确 无账号无法判断订单在哪个表
    """
    FizAssert(in_out="oversea").assert_order_info(ssoid, order_info["pay_req_id"], amount*100, amount*100)
    """
    【4】. 检查trade_order表信息是否正确 海外目前不校验
    """
    """
    【5】. 检查通知表信息是否正确
    """
    FizAssert(in_out="oversea").assert_notify(order_info["partner_order"])


if __name__ == '__main__':
    skip_pay(500, 500)
