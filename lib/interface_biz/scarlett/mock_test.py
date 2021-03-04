#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/4 9:43
# comment:
from flask import Flask, request
from lib.common.logger.logging import Logger
from lib.common_biz.order_random import RandomOrder
from lib.interface_biz.scarlett.json_to_xml import qq_mock_refund_to_xml, wx_mock_refund_to_xml

logger = Logger('mock-scarlet').get_logger()


def qq_refund_mock():
    qq_refund_info = {
        "return_code": "SUCCESS",
        "return_msg": "SUCCESS",
        "retcode": "0",
        "retmsg": "ok",
        "appid": "1104946420",
        "mch_id": "1282256301",
        "nonce_str": RandomOrder(32).random_string(),
        "openid": "0D4E5B0D1AE1605ADD7EECFCA611DC84",
        "out_refund_no": RandomOrder(32).random_num(),
        # 支付订单号
        "out_trade_no": "",
        "refund_channel": "ORIGINAL",
        "refund_fee": "1",
        "refund_id": RandomOrder(32).random_num(),
        "result_code": "SUCCESS",
        "sign": "",
        "total_fee": "1",
        # 回调id
        "transaction_id": ""
    }
    logger.info("mock报文：{}".format(qq_refund_info))
    return qq_mock_refund_to_xml(qq_refund_info, "46b3da6ee122993430adb1f7e20c4327")


def wx_refund_mock_scarlett():
    wx_refund_info = {
        "return_code": "SUCCESS",
        "return_msg": "OK",
        "appid": "wx93eea96ecc33f168",
        "mch_id": "1259634601",
        "nonce_str": "D4u7oaArJWL62aY2",
        "sign": "",
        "result_code": "SUCCESS",
        # 支付回调id
        "transaction_id": "",
        # 支付订单号
        "out_trade_no": "",
        "out_refund_no": RandomOrder(32).random_num(),
        "refund_id": RandomOrder(29).random_num(),
        "refund_channel": "",
        "refund_fee": "1",
        "coupon_refund_fee": "0",
        "total_fee": "1",
        "cash_fee": "1",
        "coupon_refund_count": "0",
        "cash_refund_fee": "1"
    }
    logger.info("mock报文：{}".format(wx_refund_info))
    return wx_mock_refund_to_xml(wx_refund_info, "3007b2945cab4fd994341dc6edb65f33")


app = Flask(__name__)


@app.route("/qq_refund", methods=["GET", "POST"])
def qq_refund():
    """
    :return:
    """
    if request.method == "POST":
        return qq_refund_mock()
    if request.method == 'GET':
        return qq_refund_mock()


@app.route("/wx_refund", methods=["GET", "POST"])
def wx_refund():
    if request.method == "POST":
        return wx_refund_mock_scarlett()
    if request.method == 'GET':
        return wx_refund_mock_scarlett()


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8888)