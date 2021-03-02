#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/9 15:11
# comment:
from lib.common.algorithm.md5 import md5
from lib.common_biz.sign import Sign


def wx_normal_pay_to_xml(scarlet_wx_pay, md5_key):
    """
    微信普通支付xml格式转换
    :return:
    """
    scarlet_wx_pay['sign'] = md5(Sign(scarlet_wx_pay).join_asc_have_key("&key=") + md5_key)
    str_xml = '<xml>'
    for item in scarlet_wx_pay:
        if item != "total_fee":
            str_xml += "<" + str(item) + ">" + "<![CDATA[" + str(scarlet_wx_pay[item]) + "]]>" + "</" + str(
                item) + ">" + "\n"
        else:
            str_xml += "<" + str(item) + ">" + str(scarlet_wx_pay[item]) + "</" + str(item) + ">" + "\n"
    return str(str_xml) + "</xml>"


def wx_sign_to_xml(scarlet_wx_sign, md5_key):
    """
    微信签约xml格式转换
    :return:
    """
    scarlet_wx_sign['sign'] = md5(Sign(scarlet_wx_sign).join_asc_have_key("&key=") + md5_key)
    str_xml = '<xml>'
    for item in scarlet_wx_sign:
        str_xml += "<" + str(item) + ">" + str(scarlet_wx_sign[item]) + "</" + str(item) + ">" + "\n"
    return str(str_xml) + "</xml>"


def qq_pay_to_xml(scarlet_qq_pay, md5_key):
    """
    qq普通支付xml格式转换
    :param scarlet_qq_pay:
    :param md5_key:
    :return:
    """
    scarlet_qq_pay['sign'] = md5(Sign(scarlet_qq_pay).join_asc_have_key("&key=") + md5_key)
    str_xml = '<?xml version="1.0" encoding="UTF-8" ?><xml>'
    for item in scarlet_qq_pay:
        str_xml += "<" + str(item) + ">" + "<![CDATA[" + str(scarlet_qq_pay[item]) + "]]>" + "</" + str(
            item) + ">" + "\n"
    return str(str_xml) + "</xml>"


def wx_mock_refund_to_xml(wx_mock_refund_info, md5_key):
    """
    微信mock方式，xml格式转换
    :return:
    """
    wx_mock_refund_info['sign'] = md5(Sign(wx_mock_refund_info).join_asc_have_key("&key=") + md5_key)
    print(Sign(wx_mock_refund_info).join_asc_have_key("&key=") + md5_key)
    str_xml = "<xml>"
    for item in wx_mock_refund_info:
        if item in ["refund_fee", "coupon_refund_fee", "total_fee", "cash_fee", "coupon_refund_count", "cash_refund_fee"]:
            str_xml += "<" + str(item) + ">" + str(wx_mock_refund_info[item]) + "</" + str(item) + ">" + "\n"
        else:
            str_xml += "<" + str(item) + ">" + "<![CDATA[" + str(wx_mock_refund_info[item]) + "]]>" + "</" + str(
                item) + ">" + "\n"
    return str(str_xml) + "</xml>"


def qq_mock_refund_to_xml(qq_refund_mock_info, md5_key):
    """
    qq渠道mock方式，xml格式转换
    :return:
    """
    qq_refund_mock_info['sign'] = md5(Sign(qq_refund_mock_info).join_asc_have_key("&key=") + md5_key)
    print(Sign(qq_refund_mock_info).join_asc_have_key("&key=") + md5_key)
    str_xml = '<?xml version="1.0" encoding="UTF-8" ?><xml>'
    for item in qq_refund_mock_info:
        str_xml += "<" + str(item) + ">" + "<![CDATA[" + str(qq_refund_mock_info[item]) + "]]>" + "</" + str(
                item) + ">" + "\n"
    return str(str_xml) + "</xml>"

