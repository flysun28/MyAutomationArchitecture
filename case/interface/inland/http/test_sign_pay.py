'''
Created on 2021年5月25日
@author: 80319739
'''
import os
import re
import time
import pytest
from lib.common.case_processor.entry import src_case_file
from lib.common_biz.json_request import (http_encjson_request, 
                                         get_check_http_json_result_positive,
                                         get_check_http_json_result_negative)
from lib.common.utils.misc_utils import timeit

case_file = src_case_file(__file__)
url = case_file.url


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
    try:
        result = http_encjson_request(case, sheetname, url)
        get_check_http_json_result_positive(case, result)
        case.is_passed = 'passed'
    finally:
        case_file.update_req(case.name, case.req_params)
        case_file.update_actual(case.name, result)


@pytest.mark.full
@pytest.mark.negative    
@pytest.mark.parametrize('case', case_file.negative_cases)
def test_inland_negative(case, sheetname):
    try:
        result = http_encjson_request(case, sheetname, url)
        get_check_http_json_result_negative(case, result)
        case.is_passed = 'passed'
    finally:
        case_file.update_req(case.name, case.req_params)
        case_file.update_actual(case.name, result)


if __name__ == '__main__':
    argv = ['-vsx', '--timeout=300', '--ff', #'--fixtures-per-test',
#             '--cov='+os.getcwd(), '--cov-report=html', 
            r'--html=%s\report\report_%s.html' %(os.getcwd(), time.strftime('%Y-%m-%d', time.localtime())),
            __file__
           ]
    print(argv)
    pytest.main(argv)
