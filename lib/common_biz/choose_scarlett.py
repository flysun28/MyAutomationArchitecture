#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/24 11:36
# comment:
from lib.common_biz.find_merchant_info import find_merchant_info
from lib.interface_biz.scarlett.heepay import hee_pay_notify
from lib.interface_biz.scarlett.oversea_coda import coda_pay
from lib.interface_biz.scarlett.oversea_upay import upay_pay_scarlet
from lib.interface_biz.scarlett.qq_pay import qq_pay_scarlet
from lib.interface_biz.scarlett.szf_pay import szf_pay
from lib.interface_biz.scarlett.wxpay import wx_normal_pay_scarlet, wx_sign_scarlet


def choose_scarlett(amount, pay_type, pay_req_id, sign_type=None, contract_code=None, partner_id=None):
    """
    目前只支持微信与点卡渠道
    :param partner_id:
    :param amount: 分
    :param pay_type: 渠道
    :param pay_req_id: 支付订单号
    :param sign_type: 是否签约
    :param contract_code: 签约订单号
    :return:
    """
    wx_pay_merchant = {}
    if sign_type is None:
        if pay_type == "wxpay":
            wx_pay_merchant = find_merchant_info("wxpay", partner_id)
            wx_normal_pay_scarlet(wx_pay_merchant["merchant_no"], pay_req_id, wx_pay_merchant["app_id"], amount,
                                  wx_pay_merchant['md5_key'])
        if pay_type == "heepay":
            hee_pay_notify(pay_req_id, amount, md5_key=find_merchant_info("heepay", partner_id)['md5_key'])
        if pay_type == "qqwallet":
            qq_pay_scarlet(pay_req_id, amount, md5_key=find_merchant_info("qq_pay", partner_id)['md5_key'])
        if pay_type == "szf_pay":
            szf_pay(pay_req_id, amount, amount, md5_key=find_merchant_info("szf_pay", partner_id)['md5_key'])
        if pay_type == "codapay_paytm":
            # coda_pay回调金额为元
            coda_pay(amount, "390", "24", pay_req_id, find_merchant_info("codapay_paytm", partner_id)['md5_key'])
        if pay_type == "upay_gamecard":
            # upay回调金额为分， 未验证签名？ 此处传元
            upay_pay_scarlet(amount, pay_req_id)
    if sign_type is not None:
        if pay_type == "wxpay":
            wx_sign_scarlet(contract_code, wx_pay_merchant['sign_merchant_no'], wx_pay_merchant["sign_plan_id"],
                            wx_pay_merchant['sign_md5_key'])


if __name__ == '__main__':

    choose_scarlett(1, "upay_gamecard", "KB202103101140312086100900160822")
    choose_scarlett(1, "wxpay", "KB202103101140312086100900160822")
    # choose_scarlett(1, "wxpay", "KB", "SIGN", "SN")

    #choose_scarlett(1000, "wxpay", "KB202103111330352076075925258582", partner_id="2031")
    #choose_scarlett(1000, "qqwallet", "RM202103111318192076075925068062", partner_id="2031")
    choose_scarlett(1000, "szf_pay", "KB202103111803182076075925365662", partner_id="2031")
    # choose_scarlett(1, "wxpay", "KB", "SIGN", "SN", partner_id="2031")

