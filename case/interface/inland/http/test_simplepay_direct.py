'''
@author: 80319739
'''
import os
import re
import time
import pytest
from lib.common.case_processor.entry import src_case_file
from lib.common.utils.misc_utils import timeit
from lib.interface_biz.http.simplepay import simplepay_test_positive, simplepay_test_negative
if __name__ == '__main__':
    from lib import pardir
    os.getcwd = lambda: pardir(pardir(pardir(pardir(__file__))))

pytestmark = pytest.mark.simplepay

case_file = src_case_file(__file__)


@timeit
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
    def test_inland_positive(self, case):
        try:
            result = simplepay_test_positive(case)
            case.is_passed = 'passed'
        finally:
            # 更新到实际结果对应表格中
            case_file.update_req(case.name, case.req_params)
            case_file.update_actual(case.name, result)


@pytest.mark.full
@pytest.mark.negative
class TestInlandNegative():
    
    @pytest.mark.parametrize('case', case_file.negative_cases)
    def test_inland_negative(self, case):
        try:
            result = simplepay_test_negative(case)
            case.is_passed = 'passed'
        finally:
            # 更新到实际结果对应表格中
            case_file.update_req(case.name, case.req_params)
            case_file.update_actual(case.name, result)


if __name__ == '__main__':
    argv = ['-vs', '-m', 'positive or negative', '--timeout=300', '--ff', 
            '--cov='+os.getcwd(), '--cov-report=html', 
            r'--html=%s\report\report_%s.html' %(os.getcwd(), time.strftime('%Y-%m-%d', time.localtime())),
            __file__
           ]
    print(argv)
    pytest.main(argv)