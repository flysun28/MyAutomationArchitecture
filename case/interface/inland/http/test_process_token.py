#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/17 16:19
# comment:
import os
import re
import time
import pytest
from lib.common.case_processor.entry import src_case_file
from lib.common_biz.json_request import http_encjson_request, get_check_http_json_result_positive, get_check_http_json_result_negative

pytestmark = pytest.mark.process_token

case_file = src_case_file(__file__)
url = case_file.url


@pytest.fixture(scope='module', autouse=True, name='sheetname')
def manage_case_file():
    yield re.match('test_(\S+).py', os.path.basename(__file__), re.I).group(1)
    case_file.save()
    case_file.close()
    

@pytest.mark.smoke
@pytest.mark.full
@pytest.mark.positive
class TestInlandPositive():

    @pytest.mark.parametrize('case', case_file.positive_cases)
    def test_inland_positive(self, case, sheetname):
        try:
            result = http_encjson_request(case, sheetname, url)        
            get_check_http_json_result_positive(case, result)
        finally:
            case_file.update_actual(case.name, result)
            if result['success'] is True:
                assert len(result['data']['processToken']) > 0


@pytest.mark.full
@pytest.mark.negative
class TestInlandNegative():

    @pytest.mark.parametrize('case', case_file.negative_cases)
    def test_inland_negative(self, case, sheetname):
        try:
            result = http_encjson_request(case, sheetname, url)
            get_check_http_json_result_negative(case, result)
        finally:
            case_file.update_actual(case.name, result)
            if result['success'] is True:
                assert len(result['data']['processToken']) > 0
         


if __name__ == '__main__':
    argv = ['-vsx', '-m negative', '--timeout=300', '--ff', 
#             '--cov='+os.getcwd(), '--cov-report=html', 
            r'--html=%s\report\report_%s.html' %(os.getcwd(), time.strftime('%Y-%m-%d', time.localtime())),
            __file__
           ]
    print(argv)
    pytest.main(argv)