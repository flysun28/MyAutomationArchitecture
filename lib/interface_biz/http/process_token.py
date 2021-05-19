#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/17 16:19
# comment:
from lib.common_biz.json_request import http_json_request


def get_process_token_positive(case)-> dict:
    return http_json_request(case, "process_token", "/api/pay-flow/v290/get-process-token")