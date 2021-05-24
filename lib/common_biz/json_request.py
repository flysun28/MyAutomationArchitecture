#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/14 11:26
# comment:
import re
from lib.common.utils.globals import HTTPENCJSON_IN
from lib.common_biz.replace_parameter import replace_http_json
from lib.common.utils.misc_utils import (flatten_nested_dict, dictionary_should_contain_sub_dictionary,
                                         run_keyword_and_expect_error)


def http_json_request(case, case_sheet, url):
    '''
    1. 发送normal http请求，返回反序列化之后的response内容（jsoned）
    2. 会设置case.response为http原始response object
    :param case: case object
    :param case_sheet: sheet name
    :param url: 
    '''
    sheetname = case.ws.title
    prefix, pay_method = re.search('({}|)(\S+)'.format(case_sheet), sheetname, re.I).groups()
    if 'processToken' in case.req_params:        
        case.req_params = replace_http_json(case.req_params)
    json_resp = HTTPENCJSON_IN.post(url, case.req_params)
    case.response = HTTPENCJSON_IN.response     # http.response object
    return json_resp


def get_check_http_json_result_positive(case, result):
    assert case.response.status_code == case.status_code
    flatten_result = flatten_nested_dict(result)
    dictionary_should_contain_sub_dictionary(flatten_result, case.expected)


def get_check_http_json_result_negative(case, result):
    assert case.response.status_code == case.status_code
    flatten_result = flatten_nested_dict(result)
    run_keyword_and_expect_error('Following keys have different values',
                                 'dictionary_should_contain_sub_dictionary',
                                 flatten_result,
                                 case.expected)