#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:02
# comment:
import decimal
import time
from case.scenario.common_req import OVERSEA_RECHARGE
from lib.common.logger.logging import Logger
from lib.common.utils.globals import GlobarVar
from lib.common_biz.choose_scarlett import choose_scarlett
from lib.common_biz.fiz_assert import FizAssert, is_assert
from lib.config.country_currency import rate_coin
from lib.interface_biz.http.oversea_query_account import oversea_query_account
from lib.interface_biz.http.oversea_recharge import Recharge
req = OVERSEA_RECHARGE
logger = Logger('oversea_recharge').get_logger()


def recharge(amount, notify_amount):
    """
        【1】. 查询可币初始化余额
    """
    balance_before = oversea_query_account(req.country, GlobarVar.SSOID, req.partner_id)
    """
        【2】. 调用可币充值接口，构造渠道回调报文
    """
    order_info = Recharge(amount, amount, country=req.country, currency=req.currency, pay_type=req.pay_channel,
                          version=req.interface_version, partner_id=req.partner_id).recharge()
    time.sleep(1)
    choose_scarlett(notify_amount, req.pay_channel, order_info['pay_req_id'], partner_id=req.partner_id)
    """
        【3】.调用查询结果接口?海外无？
    """
    """
        【4】. 检查充值成功后，可币余额是否正确
    """
    rate = rate_coin[req.currency]
    cocoinRechargeAmount = round(decimal.Decimal(amount / rate), 4)
    balance_after = oversea_query_account(req.country, GlobarVar.SSOID, req.partner_id)
    try:
        # decimal.Decimal截取4位处理，与数据库保持一致
        assert balance_after == cocoinRechargeAmount + balance_before
        logger.info("可币充值成功")
    except AssertionError as e:
        logger.info("可币充值异常")
        raise e
    """
        【5】.检查订单表记录是否正确
    """
    if is_assert():
        # 订单表金额记录为分，元转分
        FizAssert(in_out="oversea").assert_order_info(req.ssoid, order_info['pay_req_id'],
                                                      notify_amount*100, notify_amount*100,
                                                      kb_spent=None, vou_amount=None)
        """
            【6】. 检查trade order表记录是否正确，海外无
        """
        """
            【7】. 检查tb_recharge表记录是否正确, 海外无
        """
        # FizAssert(in_out="oversea").assert_tb_recharge(ssoid, order_info['pay_req_id'], amount)


if __name__ == '__main__':
    recharge(1000, 1000)
