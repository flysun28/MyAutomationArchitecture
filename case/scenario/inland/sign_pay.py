#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:04
# comment:
import random
from lib.common.utils.globals import GlobarVar
from lib.common_biz.biz_db_operate import update_sign_status, get_contract_code
from lib.common_biz.choose_scarlett import choose_scarlett
from lib.common_biz.find_key import GetKey
from lib.common_biz.find_merchant_info import FindMerchant
from lib.common_biz.fiz_assert import FizAssert
from lib.common_biz.order_random import RandomOrder
from lib.interface_biz.http.auto_re_new import AutoRenew
from lib.interface_biz.http.query_result import queryResult
from lib.interface_biz.scarlett.wxpay import wx_sign_scarlet, wx_normal_pay_scarlet


merchant_info = FindMerchant("2031").find_app_id_merchant_sign("wxpay")
md5_key = GetKey("").get_md5_key_from_merchant(merchant_info["app_id"], merchant_info["merchant_no"], "wxpay")
SSOID = GlobarVar.SSOID


def sign_pay(amount, notify_amount, pay_type="wxpay"):
    """
    签约支付
    :param notify_amount:
    :param pay_type:
    :param amount:  分
    :return:
    """
    """
        【1】. 更新数据库状态为UNSIGN
    """
    update_sign_status(SSOID, pay_type)
    """
        【2】. 调用签约支付下单接口，构造支付与签约回调报文
    """
    order_info = AutoRenew().auto_renew(amount=amount/100)
    sign_request_id = order_info['pay_req_id']
    contract_code = get_contract_code(sign_request_id)
    # 签约回调
    # wx_sign_scarlet(contract_code, merchant_info['merchant_no'], merchant_info["plan_id"],
     #               md5_key)
    choose_scarlett(1, "wxpay", "", "SIGN", contract_code)
    # 支付回调
    #wx_normal_pay_scarlet(merchant_info["merchant_no"], order_info["pay_req_id"], merchant_info["app_id"], amount, md5_key)
    choose_scarlett(notify_amount, pay_type, order_info['pay_req_id'])
    """
    
        【3】. 查询支付结果
    """
    assert str(queryResult(order_info["pay_req_id"])) == "2002"
    """
        【4】. 查询order表记录是否正确
    """
    FizAssert().assert_order_info(SSOID, order_info["pay_req_id"], amount, amount)
    """
        【5】. 查询trade_order表记录是否正确
    """
    FizAssert().assert_trade_order(SSOID, order_info["pay_req_id"], amount, amount)
    """
        【6】.检查autorenew_sign_info表信息
    """
    FizAssert().assert_auto_renew_sign_info(SSOID, pay_type)
    """
        【7】.检查autorenew_sign_record表信息
    """
    FizAssert().assert_auto_renew_sign_record(sign_request_id)
    """
        【8】.检查表notify_info信息(签约与支付， 漏了一个通知， 待补齐)
    """
    FizAssert().assert_notify(order_info["partner_code"])


if __name__ == '__main__':
    sign_pay(1, 1)
