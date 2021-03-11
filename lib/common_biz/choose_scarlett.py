#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/24 11:36
# comment:
from lib.common.file_operation.config_operation import Config
from lib.common_biz.file_path import key_path
from lib.common_biz.find_key import GetKey
from lib.common_biz.find_merchant_info import FindMerchant
from lib.config.path import merchant_path
from lib.interface_biz.scarlett.heepay import hee_pay_notify
from lib.interface_biz.scarlett.qq_pay import qq_pay_scarlet
from lib.interface_biz.scarlett.szf_pay import szf_pay
from lib.interface_biz.scarlett.wxpay import wx_normal_pay_scarlet, wx_sign_scarlet

merchant_info = FindMerchant("2031").find_app_id_merchant("wxpay")
md5_key = GetKey("").get_md5_key_from_merchant(merchant_info["app_id"], merchant_info["merchant_no"], "wxpay")

merchant_info_sign = FindMerchant("2031").find_app_id_merchant_sign("wxpay")
md5_key_sign = GetKey("").get_md5_key_from_merchant(merchant_info["app_id"], merchant_info["merchant_no"], "wxpay")

qq_pay_merchant = Config(merchant_path).as_dict('qq_pay')
szf_pay_merchant = Config(merchant_path).as_dict('szf_pay')


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
            hee_pay_notify(pay_req_id, amount)
        if pay_type == "qqwallet":
            qq_pay_scarlet(pay_req_id, amount, md5_key=qq_pay_merchant['md5_key'])
        if pay_type == "szf_pay":
            szf_pay(pay_req_id, amount, amount, md5_key=szf_pay_merchant['md5_key'])

    if sign_type is not None:
        if pay_type == "wxpay":
            wx_sign_scarlet(contract_code, merchant_info_sign['merchant_no'], merchant_info_sign["plan_id"], md5_key_sign)


if __name__ == '__main__':
    choose_scarlett(1000, "wxpay", "RM20210304095657207607592506772t")
    # choose_scarlett(1, "wxpay", "KB", "SIGN", "SN")