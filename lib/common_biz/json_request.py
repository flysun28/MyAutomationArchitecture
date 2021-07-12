# -*- encoding:utf-8 *-*
# author:80319739
# datetime:2021/5/14 11:26
from functools import partial
from lib.common_biz.replace_parameter import replace_http_json
from lib.common.utils.misc_utils import (flatten_nested_dict, dictionary_should_contain_sub_dictionary,
                                         run_keyword_and_expect_error)
from lib.common.utils.globals import HTTPENCJSON_IN, HTTPJSON_IN


def http_encjson_request(case, case_sheet, url, session=HTTPENCJSON_IN, process_token=None):
    '''
    1. 发送normal http请求，返回反序列化之后的response内容（jsoned）
    2. 会设置case.response为http原始response object
    :param case: case object
    :param case_sheet: expected sheet name
    :param url: 
    '''
    sheetname = case.ws.title
    assert sheetname == case_sheet, 'CaseFile sheetname: {} != expected: {}'.format(sheetname, case_sheet)
    # 替换case.req_params中的processToken    
    if 'processToken' in case.req_params:
        case.req_params = replace_http_json(case.req_params, processToken=process_token)    
    json_resp = session.post(url, case.req_params)
    case.response = session.response     # http.response object
    return json_resp


def get_check_http_json_result_positive(case, result):
    assert case.response.status_code == case.status_code
    flatten_result = flatten_nested_dict(result)
    dictionary_should_contain_sub_dictionary(flatten_result, case.expected)
    case.is_passed = 'passed'


def get_check_http_json_result_negative(case, result):
    assert case.response.status_code == case.status_code
    flatten_result = flatten_nested_dict(result)
    run_keyword_and_expect_error('Following keys have different values',
                                 'dictionary_should_contain_sub_dictionary',
                                 flatten_result,
                                 case.expected)
    case.is_passed = 'passed'


http_json_request = partial(http_encjson_request, session=HTTPJSON_IN)