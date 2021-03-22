#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
from lib.common.logger.logging import Logger
from lib.common_biz.choose_scarlett import choose_scarlett
from lib.common_biz.fiz_assert import FizAssert, is_assert
from lib.interface_biz.http.query_result import queryResult
from lib.interface_biz.http.simplepay import SimplePay
from case.scenario.common_req import DIRECT_PAY

logger = Logger('direct_pay').get_logger()

req = DIRECT_PAY
fizassert = FizAssert()


def direct_pay(amount, notify_amount):
    """
    :param notify_amount: 分
    :param amount: 分
    :return:
    """
    """
    【1】. 调用直扣接口，构造渠道回调报文
    """
    order = SimplePay(req.pay_channel, amount, req.partner_id, req.app_version, req.interface_version, "",
                      req.notify_url).direct_pay()
#     sleep(1)
    choose_scarlett(notify_amount, req.pay_channel, order['pay_req_id'], partner_id=req.partner_id)
    """
    【2】. 调用查询结果接口
    """
    assert str(queryResult(order["pay_req_id"], "direct")) == "2002"
    if is_assert():
        """
        【3】. 检查order_info表信息是否正确
        """
        fizassert.assert_order_info(req.ssoid, order["pay_req_id"], amount, amount)
        """
        【4】. 检查trade_order表信息是否正确
        """
        fizassert.assert_trade_order(req.ssoid, order["pay_req_id"], amount, amount)
        """
        【5】. 检查通知表信息是否正确
        """
        fizassert.assert_notify(order["partner_order"])


if __name__ == '__main__':
    direct_pay(1, 1)
    # direct_pay(2, 1)
