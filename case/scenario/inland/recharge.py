#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:02
# comment:
import decimal
import time
from case.scenario.common_req import RECHARGE_PAY
from lib.common.logger.logging import Logger
from lib.common.utils.globals import GlobalVar
from lib.common_biz.choose_scarlett import choose_scarlett
from lib.common_biz.fiz_assert import FizAssert, is_assert
from lib.interface_biz.http.gateway_query_account import query_account
from lib.interface_biz.http.query_result import queryResult
from lib.interface_biz.http.simplepay import SimplePay
from lib.common.exception import WaitUntilTimeOut

logger = Logger('recharge').get_logger()

req = RECHARGE_PAY


def recharge(amount, notify_amount):
    """
    :param pay_type:
    :param notify_amount:
    :param amount: 分
    :return:
    """
    """
        【1】. 查询可币初始化余额, 并初始化为0
    """
    balance_before = query_account(GlobalVar.SSOID)
    """
        【2】. 调用可币充值接口，构造渠道回调报文
    """
    pay_req_id = SimplePay(req.pay_channel, amount, req.partner_id, req.app_version, req.interface_version, "",
                      req.notify_url).recharge()
    time.sleep(1)
    choose_scarlett(notify_amount, req.pay_channel, pay_req_id, partner_id=req.partner_id)
    """
        【3】.调用查询结果接口
    """    
    with WaitUntilTimeOut('str(queryResult(pay_req_id)) == "2002"') as wt:
        wt.wait()
    """
        【4】. 检查充值成功后，可币余额是否正确
    """
    balance_after = query_account(GlobalVar.SSOID)
    try:
        # decimal.Decimal截取4位处理，与数据库保持一致
        assert balance_after == balance_before + amount
        logger.info("可币充值成功")
    except AssertionError as e:
        logger.info("可币充值异常")
        raise e
    """
        【5】.检查订单表记录是否正确
    """
    if is_assert():
        FizAssert().assert_order_info(req.ssoid, pay_req_id, amount, amount)
        """
            【6】. 检查trade order表记录是否正确
        """
        FizAssert().assert_trade_order(req.ssoid, pay_req_id, amount, amount)
        """
            【7】. 检查tb_recharge表记录是否正确
        """
        FizAssert().assert_tb_recharge(req.ssoid, pay_req_id, amount)


if __name__ == '__main__':
    a = recharge(5, 5)



