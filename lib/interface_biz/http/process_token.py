#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/17 16:19
# comment:
from lib.common_biz.json_request import http_json_request
from lib.common.utils.misc_utils import flatten_nested_dict, run_keyword_and_expect_error, dictionary_should_contain_sub_dictionary


def get_process_token_positive(case)-> dict:
    try:
        result = http_json_request(case, "process_token", "/api/pay-flow/v290/get-process-token")
    except:
        raise
    else:        
        res4check = flatten_nested_dict(result)
        dictionary_should_contain_sub_dictionary(res4check, case.expected)        
        return result


def get_process_token_negative(case):
    try:
        result = http_json_request(case, "process_token", "/api/pay-flow/v290/get-process-token")
    except:
        raise
    else:
        res4check = flatten_nested_dict(result)
        run_keyword_and_expect_error('Following keys have different values',
                                     'dictionary_should_contain_sub_dictionary',
                                     res4check,
                                     case.expected)
        return result