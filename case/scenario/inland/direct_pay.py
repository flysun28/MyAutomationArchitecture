#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
import time
from lib.common.logger.logging import Logger
from lib.common_biz.choose_scarlett import choose_scarlett
from lib.common_biz.fiz_assert import is_assert, ASSERTION_IN
from lib.interface_biz.http.query_result import queryResult
from lib.interface_biz.http.simplepay import SimplePay
from case.scenario.common_req import DIRECT_PAY


logger = Logger('direct_pay').get_logger()

req = DIRECT_PAY


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
    start = time.perf_counter()
    while time.perf_counter() - start < 5:
        try:
            query_res = queryResult(order["pay_req_id"], pass_type="direct")
            assert query_res == '2002', '%s != 2002' % query_res
        except Exception as e:
            exc_value = e
            time.sleep(0.5)
        else:
            break
    else:
        raise TimeoutError('查询签约支付结果超时5s: %s!' %exc_value)
    if is_assert():
        """
        【3】. 检查order_info表信息是否正确
        """
        ASSERTION_IN.assert_order_info(req.ssoid, order["pay_req_id"], amount, amount)
        """
        【4】. 检查trade_order表信息是否正确
        """
        ASSERTION_IN.assert_trade_order(req.ssoid, order["pay_req_id"], amount, amount)
        """
        【5】. 检查通知表信息是否正确
        """
        ASSERTION_IN.assert_notify(order["partner_order"], amount)



if __name__ == '__main__':
    direct_pay(1, 1)
#     paycenter_direct_pay()
