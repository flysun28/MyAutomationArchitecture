#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/24 11:36
# comment:
from lib.common_biz.find_key import GetKey
from lib.common_biz.find_merchant_info import FindMerchant
from lib.interface_biz.scarlett.heepay import hee_pay_notify
from lib.interface_biz.scarlett.qq_pay import qq_pay_scarlet
from lib.interface_biz.scarlett.wxpay import wx_normal_pay_scarlet, wx_sign_scarlet

merchant_info = FindMerchant("2031").find_app_id_merchant("wxpay")
md5_key = GetKey("").get_md5_key_from_merchant(merchant_info["app_id"], merchant_info["merchant_no"], "wxpay")

merchant_info_sign = FindMerchant("2031").find_app_id_merchant_sign("wxpay")
md5_key_sign = GetKey("").get_md5_key_from_merchant(merchant_info["app_id"], merchant_info["merchant_no"], "wxpay")


def choose_scarlett(amount, pay_type, pay_req_id, sign_type=None, contract_code=None):
    """
    目前只支持微信与点卡渠道
    :param amount: 分
    :param pay_type: 渠道
    :param pay_req_id: 支付订单号
    :param sign_type: 是否签约
    :param contract_code: 签约订单号
    :return:
    """
    if sign_type is None:
        if pay_type == "wxpay":
            wx_normal_pay_scarlet(merchant_info["merchant_no"], pay_req_id, merchant_info["app_id"], amount,
                                  md5_key)
        if pay_type == "heepay":
            hee_pay_notify(pay_req_id, amount/100)
        if pay_type == "qqwallet":
            qq_pay_scarlet(pay_req_id, amount/100)
    if sign_type is not None:
        if pay_type == "wxpay":
            wx_sign_scarlet(contract_code, merchant_info_sign['merchant_no'], merchant_info_sign["plan_id"], md5_key_sign)


if __name__ == '__main__':
    choose_scarlett(1, "wxpay", "KB202103101140312086100900160822")
    # choose_scarlett(1, "wxpay", "KB", "SIGN", "SN")