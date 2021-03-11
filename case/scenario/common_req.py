#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/27 16:04
# comment:
import random
from lib.common.utils.globals import GlobarVar


class Order:
    ssoid = GlobarVar.SSOID

    def __init__(self, amount=0, notify_amount=0, country="CN", currency="CNY", pay_channel="wxpay", partner_id="2031",
                 notify_url=str(GlobarVar.URL_PAY_IN) + "/notify/receiver", app_version=260,
                 interface_version="12.0", version_exp="12.0", renewProductCode="20310001"):
        #  "http://secure.pay-test2.wanyol.com"
        self.amount = amount
        self.notify_amount = notify_amount
        self.pay_channel = pay_channel
        self.partner_id = partner_id
        self.renewProductCode = renewProductCode
        self.notify_url = notify_url
        self.app_version = app_version
        self.interface_version = interface_version
        self.version_exp = version_exp
        self.country = country
        self.currency = currency


class Vou:
    def __init__(self, vouConditionAmount, vouAmount, country="", currency="", partner_id="2031", vouId=0, vouType=2,
                 couponType="KB_COUPON", couponDiscountType="XIAOFEI", factor=""):
        self.partner_id = partner_id
        self.vouId = vouId
        # "KB_COUPON"
        self.couponType = couponType
        # 数字类型
        self.vouType = vouType
        # "DIKOU" 文字类型
        self.couponDiscountType = couponDiscountType
        self.vouConditionAmount = vouConditionAmount
        self.vouAmount = vouAmount
        self.factor = factor
        self.country = country
        self.currency = currency


class KB:
    def __init__(self, country, currency, kb_amount):
        self.country = country
        self.currency = currency
        self.kb_amount = kb_amount


# 分
vou_amount = 1
# 国内
DIRECT_PAY = Order()
NO_LOGIN_PAY = Order(partner_id="72724313")
ONLY_SIGN = Order(interface_version="1.0")
RECHARGE_PAY = Order()
SIGN_PAY = Order()
EXPEND_PAY = Order(interface_version="6.0")
RECHARGE_SPEND_PAY = Order()
VOU_INLAND = Vou(vouConditionAmount=str(0), vouAmount=str(vou_amount))

# 海外
OVERSEA_SKIP_PAY = Order(interface_version="15.0", country="IN", currency="INR", pay_channel="codapay_paytm")
OVERSEA_NO_LOGIN = Order(interface_version="15.0", country="IN", currency="IN", pay_channel="codapay_paytm")
OVERSEA_RECHARGE = Order(country="VN", currency="VND", pay_channel="upay_gamecard", interface_version="15.0")
OVERSEA_RECHARGE_SPEND = Order(country="VN", currency="VND", pay_channel="upay_gamecard", interface_version="15.0")
OVERSEA_SPEND = Order(interface_version="15.0", country="VN", currency="VND")
VOU_OVERSEA = Vou(vouConditionAmount=str(vou_amount), vouAmount=str(vou_amount - 0.01), country="VN", currency="VND")


if __name__ == '__main__':
    pass
