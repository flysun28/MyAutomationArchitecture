#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:03
# comment:
from lib.common.utils.globals import GlobarVar
from lib.common_biz.biz_db_operate import get_contract_code, update_sign_status
from lib.common_biz.find_key import GetKey
from lib.common_biz.find_merchant_info import FindMerchant
from lib.common_biz.fiz_assert import FizAssert
from lib.common_biz.order_random import RandomOrder
from lib.interface_biz.http.auto_re_new import AutoRenew
from lib.interface_biz.http.query_result import queryResult
from lib.interface_biz.scarlett.wxpay import wx_sign_scarlet
merchant_info = FindMerchant("2031").find_app_id_merchant_sign("wxpay")
md5_key = GetKey("").get_md5_key_from_merchant(merchant_info["app_id"], merchant_info["merchant_no"], "wxpay")
SSOID = GlobarVar.SSOID


def only_sign(pay_type):
    """
    :return:
    """
    """
    【1】. 更新数据库状态为UNSIGN
    """
    update_sign_status(SSOID, pay_type)
    """
    【2】. 调用签约接口，构造渠道回调报文
    """
    sign_order_info = AutoRenew().only_sign()
    sign_request_id = sign_order_info['pay_req_id']
    contract_code = get_contract_code(sign_request_id)
    wx_sign_scarlet(contract_code, RandomOrder(10).random_num(), merchant_info['merchant_no'], merchant_info["plan_id"], md5_key)
    """
    【3】. 查询支付结果
    """
    assert str(queryResult(sign_request_id, "SIGN")) == "0000"
    """
    【4】.检查order表信息，无记录
    """
    """
    【5】.检查trade_order表信息，无记录
    """
    """
    【6】.检查autorenew_sign_info表信息
    """
    FizAssert().assert_auto_renew_sign_info(SSOID, pay_type)
    """
    【7】.检查autorenew_sign_record表信息
    """
    FizAssert().assert_auto_renew_sign_record(sign_request_id)
    """
    【8】.检查表notify_info信息
    """
    FizAssert().assert_notify(sign_order_info["partner_code"])


if __name__ == '__main__':
    only_sign("wxpay")
