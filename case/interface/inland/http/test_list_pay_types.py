#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/17 15:52
# comment:
import re
import os
import time
import pytest
from lib.common.case_processor.entry import src_case_file
from lib.common.utils.globals import HTTPENCJSON_IN, GlobalVar
from lib.common.utils.misc_utils import timeit
from lib.common_biz.json_request import http_encjson_request, get_check_http_json_result_positive, get_check_http_json_result_negative
from lib.common_biz.replace_parameter import replace_http_json_req


pytestmark = pytest.mark.list_pay_types

case_file = src_case_file(__file__)
url = case_file.url
HTTPENCJSON_IN.header['X-APP']['appPackage'] = 'com.oppo.usercenter'
HTTPENCJSON_IN.header['X-APP']['appVersion'] = '280'


@timeit
@pytest.fixture(scope='module', autouse=True, name='sheetname')
def manage_case_file():
    yield re.match('test_(\S+).py', os.path.basename(__file__), re.I).group(1)
    case_file.save()
    case_file.close()
    

@pytest.mark.smoke
@pytest.mark.full
@pytest.mark.positive
@pytest.mark.parametrize('case', case_file.positive_cases)
def test_inland_positive(case, sheetname):
    case.req_params = replace_http_json_req(case.req_params)
    try:
        result = http_encjson_request(case, sheetname, url)
        get_check_http_json_result_positive(case, result)
    finally:
        case_file.update_req(case.name, case.req_params)
        case_file.update_actual(case.name, result)


@pytest.mark.full
@pytest.mark.negative    
@pytest.mark.parametrize('case', case_file.negative_cases)
def test_inland_negative(case):
    case.req_params = replace_http_json_req(case.req_params)
    if case.name.strip() == 'processToken传入不正确':
        case.req_params['processToken'] = ''
    try:
        result = HTTPENCJSON_IN.post(url, case.req_params)
        case.response = HTTPENCJSON_IN.response     # http.response object
        get_check_http_json_result_negative(case, result)
    finally:
        case_file.update_req(case.name, case.req_params)
        case_file.update_actual(case.name, result)


if __name__ == '__main__':
    argv = ['-vs', '--timeout=300', '--ff', 
#             '--cov='+os.getcwd(), '--cov-report=html', 
            r'--html=%s\report\report_%s.html' %(os.getcwd(), time.strftime('%Y-%m-%d', time.localtime())),
            __file__
           ]
    print(argv)
    pytest.main(argv)