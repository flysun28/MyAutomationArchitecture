#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:02
# comment:
import time
from lib.common.logger.logging import Logger
from lib.common.utils.globals import GlobarVar
from lib.common_biz.biz_db_operate import get_balance, oversea_get_coin_rate
from lib.common_biz.fiz_assert import FizAssert
from lib.config.country_currency import currency
from lib.interface_biz.dubbo.oversea_coin import Coin
from lib.interface_biz.http.oversea_recharge import Recharge
from lib.interface_biz.scarlett.oversea_upay import upay_pay_scarlet

ssoid = GlobarVar.SSOID
logger = Logger('oversea_recharge').get_logger()


def recharge(amount, notify_amount, country):
    """
        【1】. 查询可币初始化余额, 并置为0
    """
    balance_before = get_balance(ssoid, country=country, in_out="oversea")
    Coin().cocoin_pay_out(ssoid, country, str(balance_before))
    """
        【2】. 调用可币充值接口，构造渠道回调报文
    """
    order_info = Recharge(amount, amount).recharge()
    time.sleep(1)
    upay_pay_scarlet(notify_amount, order_info['pay_req_id'])
    """
        【3】.调用查询结果接口?海外无？
    """
    """
        【4】. 检查充值成功后，可币余额是否正确
    """
    rate = oversea_get_coin_rate(currency[country])
    cocoinRechargeAmount = (amount / rate)/100
    balance_after = get_balance(ssoid, country=country, in_out="oversea")
    try:
        # decimal.Decimal截取4位处理，与数据库保持一致
        print(balance_after, cocoinRechargeAmount, rate)
        assert balance_after == cocoinRechargeAmount
        logger.info("可币充值成功")
    except AssertionError as e:
        logger.info("可币充值异常")
        raise e
    """
        【5】.检查订单表记录是否正确
    """
    FizAssert(in_out="oversea").assert_order_info(ssoid, order_info['pay_req_id'], amount, amount*100)
    """
        【6】. 检查trade order表记录是否正确，海外无
    """
    """
        【7】. 检查tb_recharge表记录是否正确, 海外无
    """
    # FizAssert(in_out="oversea").assert_tb_recharge(ssoid, order_info['pay_req_id'], amount)


if __name__ == '__main__':
    recharge(1000, 1000, "VN")