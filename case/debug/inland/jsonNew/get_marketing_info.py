#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/13 18:28
# comment:
from lib.common.utils.globals import pyobj_resp
from lib.common_biz.replace_parameter import replace_http_json
from lib.interface_biz.http.pay_pass import get_process_token
processToken = get_process_token()

case_data = {
    "processToken": "Pskac8goWdnJD3Xj4DeSV9",
    "partnerId": "5456925",
    "orderAmount": "10000",
    "factor": ""
}
result = pyobj_resp.post('/api/marketing/v290/get-marketing-info', case_data)
print(result)