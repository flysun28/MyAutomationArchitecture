import sys
import re
from functools import wraps
from types import ModuleType
from lib.common.session.http.protobuf import ProtoBuf
from lib.common.utils.globals import HTTPJSON_IN
from lib.common_biz.replace_parameter import ReplaceParams
from lib.common_biz.pbjson import pb2dict
from lib.common.utils.misc_utils import flatten_nested_dict, dictionary_should_contain_sub_dictionary, run_keyword_and_expect_error


def _qualify_pb_src(func):
    '''
    将func传参`pb_src`转为模块类型
    '''
    @wraps(func)
    def wrapper(case, pb_src):
        if isinstance(pb_src, str):
            pb_module = eval(pb_src)
        elif isinstance(pb_src, ModuleType):
            pb_module = pb_src
        return func(case, pb_module)
    return wrapper


@_qualify_pb_src
def http_pb_request(case, pb_src):
    sheetname = case.ws.title
    prefix, pay_method = re.search('(simplepay_|)(\S+)', sheetname, re.I).groups()
    repl = ReplaceParams(case.req_params)
    if prefix:
        req = repl.replace_native(pay_method)
    raw_response = ProtoBuf(pb_src).runner(HTTPJSON_IN.prefix + '/plugin/post/simplepay', 'Request', req, flag=0)
    case.response = raw_response


@_qualify_pb_src
def get_check_pb_result_positive(case, pb_src):
    assert case.response.status_code == case.status_code
    result = ProtoBuf(pb_src).parser('Result', case.response)
    # 转字典，方便比较
    dict_result = pb2dict(result)
    res4check = flatten_nested_dict(dict_result)
    dictionary_should_contain_sub_dictionary(res4check, case.expected)
    return dict_result


@_qualify_pb_src
def get_check_pb_result_negative(case, pb_src):
    assert case.response.status_code == case.status_code
    result = ProtoBuf(pb_src).parser('Result', case.response)
    # 转字典，方便比较
    dict_result = pb2dict(result)
    res4check = flatten_nested_dict(dict_result)
    run_keyword_and_expect_error('Following keys have different values',
                                 'dictionary_should_contain_sub_dictionary',
                                 res4check,
                                 case.expected)
    return dict_result

