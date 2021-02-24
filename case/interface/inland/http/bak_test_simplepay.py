'''
@author: 80319739
'''
import os
import re
import pytest
from lib.common.case_processor.entry import CaseFile
from lib.common.utils.globals import CASE_SRCFILE_ROOTDIR
from lib.common.utils.misc_utils import dictionary_should_contain_sub_dictionary
from lib.interface_biz.http.simplepay import http_pb_simplepay

pytestmark = pytest.mark.simplepay
# basename = os.path.basename(__file__)
# interface_name = re.search('test_(\w+)', basename, re.I).group(1)
# case_file_dir = os.path.join(CASE_FILE_ROOTDIR, 'http', )
# case_file_obj = None

@pytest.fixture(scope='module', autouse=True)
def module_setup_and_teardown():
    print('into module setup..........')
    case_file_dir = os.path.join(CASE_SRCFILE_ROOTDIR, 'http')
    basename = os.path.basename(__file__)
    interface_name = re.search('test_(\w+)', basename, re.I).group(1)
    case_file_obj = CaseFile(os.path.join(case_file_dir, 'inland.xlsx'), interface=interface_name)
    yield case_file_obj
    print('into module teardown........')
    case_file_obj.save()
    case_file_obj.close()

# @pytest.fixture(scope='module', autouse=True)
# def create_case_file():
#     case_file_dir = os.path.join(CASE_SRCFILE_ROOTDIR, 'http')
#     basename = os.path.basename(__file__)
#     interface_name = re.search('test_(\w+)', basename, re.I).group(1)
#     return CaseFile(os.path.join(case_file_dir, 'inland.xlsx', interface=interface_name))


# @pytest.fixture(scope='function', autouse=True)
# def case_teardown(self, module_setup_and_teardown):
#     yield
#     module_setup_and_teardown.update_actual(self.actual_resp)

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
        
#     @pytest.mark.parametrize('case', module_setup_and_teardown.positive_cases)
    def test_inland_positive(self, module_setup_and_teardown):
        for case in module_setup_and_teardown.positive_cases:
            self.actual_resp = http_pb_simplepay(case.req_params)        
            dictionary_should_contain_sub_dictionary(self.actual_resp, case.expected)


class TestInlandNegative():
#     pytestmark = pytest.mark.full, pytest.mark.negative
    
#     @pytest.mark.parametrize('case', case_file_obj.negative_cases)
    def test_inland_negative(self, module_setup_and_teardown):
        for case in module_setup_and_teardown.positive_cases:
            self.actual_resp = http_pb_simplepay(case.req_params)
            dictionary_should_contain_sub_dictionary(self.actual_resp, case.expected)


if __name__ == '__main__':
    module_setup_and_teardown()
