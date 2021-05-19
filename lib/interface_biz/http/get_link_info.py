#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/14 15:16
# comment: 营销信息-获取跳转链接信息
from lib.common_biz.json_request import http_json_request


def get_link_info_test_positive(case)-> dict:
    return http_json_request(case, "get_link_info", "/api/marketing/v290/get-link-info")