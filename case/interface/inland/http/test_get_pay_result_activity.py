'''
Created on 2021年5月19日
@author: 80319739
'''
import os
import time
import pytest
from lib.common.case_processor.entry import src_case_file
from lib.common_biz.json_request import (http_json_request, 
                                         get_check_http_json_result_positive,
                                         get_check_http_json_result_negative)
from lib.interface_biz.http.pay_pass import get_process_token
from lib.common.utils.misc_utils import timeit

case_file = src_case_file(__file__)


@pytest.fixture(scope='module', autouse=True)
def process_token():
    return get_process_token()


@pytest.fixture(scope='module', autouse=True)
@timeit
def manage_case_file():
    yield 
    case_file.save()
    case_file.close()


@pytest.mark.smoke
@pytest.mark.full
@pytest.mark.positive
@pytest.mark.parametrize('case', case_file.positive_cases)
def test_inland_positive(case):        
    result = http_json_request(case, "get_pay_result_activity", "/api/marketing/v290/get-pay-result-activity")
    case_file.update_actual(case.name, result)
    get_check_http_json_result_positive(case, result)


@pytest.mark.full
@pytest.mark.negative    
@pytest.mark.parametrize('case', case_file.negative_cases)
def test_inland_negative(case):
    result = http_json_request(case, "get_pay_result_activity", "/api/marketing/v290/get-pay-result-activity")
    case_file.update_actual(case.name, result)
    get_check_http_json_result_negative(case, result)


if __name__ == '__main__':
    argv = ['-v', '--timeout=300', '--ff', 
#             '--cov='+os.getcwd(), '--cov-report=html', 
            r'--html=%s\report\report_%s.html' %(os.getcwd(), time.strftime('%Y-%m-%d', time.localtime())),
            __file__
           ]
    print(argv)
    pytest.main(argv)