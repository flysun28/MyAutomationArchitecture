'''
@author: 80319739
'''
import os
import time
import pytest
from lib.common.case_processor.entry import src_case_file
from lib.interface_biz.http.simplepay import simplepay_test_positive, simplepay_test_negative
if __name__ == '__main__':
    from lib import pardir
    os.getcwd = lambda: pardir(pardir(pardir(pardir(__file__))))

pytestmark = pytest.mark.simplepay

case_file = src_case_file(__file__)


@pytest.mark.smoke
@pytest.mark.full
@pytest.mark.positive
class TestInlandPositive():
    
    @pytest.mark.parametrize('case', case_file.positive_cases)
    def test_inland_positive(self, case):
        result = simplepay_test_positive(case)
        # 更新到实际结果对应表格中
        case_file.update_actual(case.name, result)
    

@pytest.mark.full
@pytest.mark.negative
class TestInlandNegative():
    
    @pytest.mark.parametrize('case', case_file.negative_cases)
    def test_inland_negative(self, case):
        result = simplepay_test_negative(case)
        # 更新到实际结果对应表格中
        case_file.update_actual(case.name, result)


if __name__ == '__main__':
    argv = ['-vs', '-m', 'positive or negative', '--timeout=300', '--ff', 
            '--cov='+os.getcwd(), '--cov-report=html', 
            r'--html=%s\report\report_%s.html' %(os.getcwd(), time.strftime('%Y-%m-%d', time.localtime())),
            __file__
           ]
    print(argv)
    pytest.main(argv)
    

