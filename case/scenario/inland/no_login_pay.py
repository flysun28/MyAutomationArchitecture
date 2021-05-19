#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
import time
from case.scenario.common_req import NO_LOGIN_PAY
from lib.common.logger.logging import Logger
from lib.common_biz.choose_scarlett import choose_scarlett
from lib.common_biz.fiz_assert import is_assert, ASSERTION_IN
from lib.interface_biz.http.query_result import queryResult
from lib.interface_biz.http.skip_pay import skip_pay
from lib.common.exception import WaitUntilTimeOut


logger = Logger('on_login_pay').get_logger()
req = NO_LOGIN_PAY


def no_login(amount, notify_amount):
    """
        疑似有的走simplepay，此处针对skippay
    :param notify_amount:
    :param pay_type:
    :param amount: 分
    :return:
    """
    """
    【1】. 调用下单接口，渠道回调构造
    """
    order = skip_pay(req.pay_channel, amount, req.partner_id, str(req.app_version), req.notify_url)
    choose_scarlett(notify_amount, req.pay_channel, order['pay_req_id'], partner_id=req.partner_id)
    """
        【2】. 调用查询结果接口
    """
    start = time.perf_counter()
    while time.perf_counter() - start < 5:
        try:
            query_res = queryResult(order["pay_req_id"], pass_type="no_login")
            assert query_res == '2002', '%s != 2002' %query_res
        except Exception as e:
            exc_value = e
            time.sleep(0.5)
        else:
            break
    else:
        raise TimeoutError('查询签约支付结果超时5s: %s!' %exc_value)
    if is_assert():
        """
            【3】. 检查order_info表信息是否正确 无账号订单分库分表规则未梳理
        """
        # FizAssert().assert_order_info(ssoid, order["pay_req_id"], amount, amount)
        """
            【4】. 检查trade_order表信息是否正确 无账号订单分库分表规则未梳理
        """
        # FizAssert().assert_trade_order(ssoid, order["pay_req_id"], amount, amount)
        """
            【5】. 检查通知表信息是否正确
        """
        ASSERTION_IN.assert_notify(order["partner_order"], amount)


if __name__ == '__main__':
    no_login(1, 1)
