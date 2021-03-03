#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/3 10:28
# comment:
from flask import Flask, request
import json
from lib.interface_biz.scarlett.qq_pay import qq_refund_mock_scarlett
from lib.interface_biz.scarlett.wxpay import wx_refund_mock_scarlett

app = Flask(__name__)


@app.route("/qq_refund", methods=["GET", "POST"])
def qq_refund():
    """
    :return:
    """
    if request.method == "POST":
        req_data = json.loads(str(request.data, encoding="utf-8"))
        return qq_refund_mock_scarlett(req_data['pay_req_id'], req_data['refund_free'], req_data['toal_free'])
    if request.method == 'GET':
        req_data = request.args
        return qq_refund_mock_scarlett(req_data['pay_req_id'], req_data['refund_free'], req_data['toal_free'])


@app.route("/wx_refund", methods=["GET", "POST"])
def wx_refund():
    if request.method == "POST":
        req_data = json.loads(str(request.data, encoding="utf-8"))
        return wx_refund_mock_scarlett(req_data['pay_req_id'], req_data['refund_fee'], req_data['total_fee'],
                                       req_data['cash_fee'], req_data['cash_refund_fee'])
    if request.method == 'GET':
        req_data = request.args
        return wx_refund_mock_scarlett(req_data['pay_req_id'], req_data['refund_fee'], req_data['total_fee'],
                                       req_data['cash_fee'], req_data['cash_refund_fee'])


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8888)
