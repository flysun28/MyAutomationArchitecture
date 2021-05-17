#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/17 15:52
# comment:
from lib.common_biz.json_request import http_json_request


def get_list_pay_types_positive(case)-> dict:
    return http_json_request(case, "list_pay_types", "/api/pay-flow/v290/list-pay-types")