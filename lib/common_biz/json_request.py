#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/14 11:26
# comment:
import re

from lib.common.utils.globals import pyobj_resp
from lib.common_biz.replace_parameter import replace_http_json


def http_json_request(case, case_sheet, url):
    sheetname = case.ws.title
    prefix, pay_method = re.search('(get_link_info|)(\S+)', sheetname, re.I).groups()
    if prefix:
        replace_http_json(case)
    raw_response = pyobj_resp.post(url, case.req_params)
    case.response = raw_response
    return case.response