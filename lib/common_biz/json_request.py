# -*- encoding:utf-8 *-*
# author:80319739
# datetime:2021/5/14 11:26
from functools import partial
from lib.common_biz.replace_parameter import replace_http_json
from lib.common.utils.misc_utils import (flatten_nested_dict, dictionary_should_contain_sub_dictionary,
                                         run_keyword_and_expect_error)
from lib.common.utils.globals import HTTPENCJSON_IN, HTTPJSON_IN
from lib.interface_biz.http.refactor.pay import update_voucher_args
from lib.common.utils.constants import voucher_type_mapping
from lib.common_biz.order_random import RandomOrder


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
    if case.req_params['goodsType'] == 'COMMON':    # 非纯充值
        case.req_params = replace_http_json(case.req_params, partnerOrder=RandomOrder(32).random_string())
    # 带券的用例，自动挑选出一个符合类型的券，替换case.req_params中的virtualAssets
    if '券' in case.name:
        vou_type = case.req_params['virtualAssets']['voucherType']
        update_voucher_args(case.req_params, voucher_type_mapping.inverse[vou_type])
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