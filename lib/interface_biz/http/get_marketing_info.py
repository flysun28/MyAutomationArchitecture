#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/17 15:46
# comment:
from lib.common_biz.json_request import http_json_request


def get_marketing_info_positive(case)-> dict:
    return http_json_request(case, "get_marketing_info", "/api/marketing/v290/get-marketing-info")