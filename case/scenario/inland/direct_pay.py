#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
import random
from lib.common.logger.logging import Logger
from lib.common.utils.globals import GlobarVar
from lib.common_biz.choose_scarlett import choose_scarlett
from time import sleep
from lib.common_biz.fiz_assert import FizAssert
from lib.interface_biz.http.query_result import queryResult
from lib.interface_biz.http.simplepay import SimplePay


ssoid = GlobarVar.SSOID
logger = Logger('direct_pay').get_logger()


def direct_pay(amount, notify_amount, pay_type="wxpay"):
    """
    :param notify_amount: 分
    :param pay_type:
    :param amount: 分
    :return:
    """
    """
        【1】. 调用直扣接口，构造渠道回调报文
    """
    order = SimplePay(pay_type, amount/100).direct_pay()
    sleep(1)
    choose_scarlett(notify_amount, pay_type, order['pay_req_id'])
    """
        【2】. 调用查询结果接口
    """
    assert str(queryResult(order["pay_req_id"], "direct")) == "2002"
    """
        【3】. 检查order_info表信息是否正确
    """
    FizAssert().assert_order_info(ssoid, order["pay_req_id"], amount, amount)
    """
        【4】. 检查trade_order表信息是否正确
    """
    FizAssert().assert_trade_order(ssoid, order["pay_req_id"], amount, amount)
    """
        【5】. 检查通知表信息是否正确
    """
    FizAssert().assert_notify(order["partner_order"])


if __name__ == '__main__':
    direct_pay(1, 1)
