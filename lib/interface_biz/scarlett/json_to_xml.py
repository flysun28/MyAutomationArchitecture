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
