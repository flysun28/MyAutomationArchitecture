#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:04
# comment:
import time
from case.scenario.common_req import SIGN_PAY
from lib.common_biz.biz_db_operate import update_sign_status, get_contract_code
from lib.common_biz.choose_scarlett import choose_scarlett
from lib.common_biz.fiz_assert import FizAssert
from lib.interface_biz.http.auto_re_new import AutoRenew
from lib.interface_biz.http.query_result import queryResult

req = SIGN_PAY


def sign_pay(amount, notify_amount):
    """
    签约支付
    :param notify_amount:
    :param amount:  分
    :return:
    """
    """
        【1】. 更新数据库状态为UNSIGN
    """
    update_sign_status(req.ssoid, req.pay_channel)
    """
        【2】. 调用签约支付下单接口，构造支付与签约回调报文
    """
    order_info = AutoRenew(req.pay_channel, req.partner_id, req.interface_version, str(req.app_version),
                                req.renewProductCode, req.notify_url).auto_renew(amount=amount)
    sign_request_id = order_info['pay_req_id']
    contract_code = get_contract_code(sign_request_id)
    # 签约回调
    choose_scarlett(1, req.pay_channel, "", "SIGN", contract_code, partner_id=req.partner_id)
    # 支付回调
    choose_scarlett(notify_amount, req.pay_channel, order_info['pay_req_id'], partner_id=req.partner_id)
    """
        【3】. 查询支付结果
    """
    start = time.perf_counter()
    while time.perf_counter() - start < 5:
        try:
            query_res = queryResult(order_info["pay_req_id"], query_type="PAY", pass_type="direct")
            assert query_res == '2002', '%s != 2002' %query_res
        except AssertionError as e:
            time.sleep(0.5)
        else:
            break
    else:
        raise TimeoutError('%s, exceed 5s!' %e)
    """
        【4】. 查询order表记录是否正确
    """
    FizAssert().assert_order_info(req.ssoid, order_info["pay_req_id"], amount, amount, vou_id="")
    """
        【5】. 查询trade_order表记录是否正确
    """
    FizAssert().assert_trade_order(req.ssoid, order_info["pay_req_id"], amount, amount)
    """
        【6】.检查autorenew_sign_info表信息
    """
    FizAssert().assert_auto_renew_sign_info(req.ssoid, req.pay_channel)
    """
        【7】.检查autorenew_sign_record表信息
    """
    FizAssert().assert_auto_renew_sign_record(sign_request_id)
    """
        【8】.检查表notify_info信息(签约与支付， 漏了一个通知， 待补齐)
    """
    # FizAssert().assert_notify(order_info["partner_code"], amount)


if __name__ == '__main__':
    sign_pay(1, 1)
