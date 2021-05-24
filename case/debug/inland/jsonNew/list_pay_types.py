#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/13 18:28
# comment:
from lib.common.utils.globals import pyobj_resp


pyobj_resp.header['X-APP']['appPackage'] = 'com.hnzh.dldlwhjx.nearme.gamecenter'
pyobj_resp.header['X-APP']['appVersion'] = '260'

case_data = {
    "processToken": "Pskac8goWdnJD3Xj4DeSV9",
    "partnerId": "2031",
    "accountExist": "Y",
    "renewal": "N",
    "acrossScreen": "N"
}
result = pyobj_resp.post('/api/pay-flow/v290/list-pay-types', case_data)
print(result)