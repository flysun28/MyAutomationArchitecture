'''
@author: 80319739
'''
import os
if __name__ == '__main__':
    os.getcwd = lambda: r'E:\SecurePaymentsAutomation\case'    
import sys
import re
import time
import pytest
from lib.common.case_processor.entry import CaseFile
from lib.common.utils.globals import CASE_SRCFILE_ROOTDIR
from lib.common.utils.misc_utils import dictionary_should_contain_sub_dictionary
from lib.interface_biz.http.simplepay import http_pb_simplepay
from importlib import reload

pytestmark = pytest.mark.simplepay


@pytest.fixture(scope='module', autouse=True)
def module_setup_and_teardown():
    print('\ninto module setup..........')
    case_file_dir = os.path.join(CASE_SRCFILE_ROOTDIR, 'http')
    basename = os.path.basename(__file__)
    interface_name = re.search('test_(\w+)', basename, re.I).group(1)
    case_file_obj = CaseFile(os.path.join(case_file_dir, 'inland.xlsx'), interface=interface_name)
    yield case_file_obj
    print('\ninto module teardown........')
    case_file_obj.save()
    case_file_obj.close()


@pytest.mark.smoke
@pytest.mark.full
@pytest.mark.positive
class TestInlandPositive():
#     pytestmark = pytest.mark.smoke, pytest.mark.full, pytest.mark.positive
    
    @pytest.fixture(scope='class', autouse=True)
    def class_setup(self):
        self.actual_resp = None
        yield
    
    @pytest.fixture(scope='function', autouse=True)
    def case_teardown(self, module_setup_and_teardown):
        yield
        module_setup_and_teardown.update_actual(self.actual_resp)

    def test_inland_positive(self, module_setup_and_teardown):
        for case in module_setup_and_teardown.positive_cases:
            self.actual_resp = http_pb_simplepay(case.req_params)
            dictionary_should_contain_sub_dictionary(self.actual_resp, case.expected)


class TestInlandNegative():
#     pytestmark = pytest.mark.full, pytest.mark.negative
    
    def test_inland_negative(self, module_setup_and_teardown):
        for case in module_setup_and_teardown.positive_cases:
            self.actual_resp = http_pb_simplepay(case.req_params)
            dictionary_should_contain_sub_dictionary(self.actual_resp, case.expected)


if __name__ == '__main__':
    argv = ['-vsx', '-m', 'positive', '--ff', '--timeout=300', 
            '--cov='+os.getcwd(), '--cov-report=html', 
            r'--html=%s\report\report_%s.html' %(os.getcwd(), time.strftime('%Y-%m-%d', time.localtime())),
            
           ]
    print(argv)
    pytest.main(argv)
    

