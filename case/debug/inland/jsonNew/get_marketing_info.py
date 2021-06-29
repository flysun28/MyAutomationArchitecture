#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/13 18:28
# comment:
from lib.common.utils.globals import pyobj_resp
from lib.interface_biz.http.pay_pass import get_process_token

processToken = get_process_token()

pyobj_resp.header['X-APP']['appVersion'] = 280

case_data = {
    "processToken": processToken,
    "partnerCode": '5456925',
    "orderAmount": 1,
    "factor": '',
    'appPackage': 'com.example.pay_demo',
    'buyPlaceId': '10001'
}
result = pyobj_resp.post('/api/marketing/v290/get-marketing-info', case_data)
print(result)
