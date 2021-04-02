#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/29 18:20
# comment:
from lib.common.utils.globals import GlobalVar

req = {
    "ssoid" : "",
    "imei": "",
    "appPackage": "",
    "model": "",
    "channelId": "",
    "clientIp": "",
    "ip": "",
    "sign": "",
    "status": "",
    "source": "",
    "payTime": "",
    "ver": "",
    "systemOrder": "",
    "payTable": "",
    "thirdId": "",
    "thirdSource": "",
    "kbVou": "",
    "spendType": "",
    "date": "",
    "amountSpent": "",
    "order": "",
    "originPrice": "",
    "paySuccessTime": "",
    "needNotify": "",
}
GlobalVar.HTTPJSON_IN.post("/nearme/PayMent", data=req)