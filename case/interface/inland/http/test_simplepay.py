'''
@author: 80319739
'''
import os
import re
import pytest
from lib.common.case_processor.entry import CaseFile
from case.interface.conftest import CASE_FILE_ROOTDIR
from lib.common.utils.misc_utils import dictionary_should_contain_sub_dictionary
from lib.interface_biz.http.simplepay import http_pb_simplepay

# basename = os.path.basename(__file__)
# interface_name = re.search('test_(\w+)', basename, re.I).group(1)
# case_file_dir = os.path.join(CASE_FILE_ROOTDIR, 'http', )

@pytest.fixture(scope='module', autouse=True)
def module_setup_and_teardown(self):
    global case_file_obj
    case_file_dir = os.path.join(CASE_FILE_ROOTDIR, 'http')
    basename = os.path.basename(__file__)
    interface_name = re.search('test_(\w+)', basename, re.I).group(1)
    case_file_obj = CaseFile(os.path.join(case_file_dir, 'inland.xlsx', interface=interface_name))
    yield
    case_file_obj.save()
    case_file_obj.close()


@pytest.fixture(scope='function', autouse=True)
def case_teardown(self):
    yield
    case_file_obj.update_actual(self.actual_resp)


class TestInlandPositive():
    pytestmark = pytest.mark.smoke, pytest.mark.functional, pytest.mark.regress, pytest.mark.positive
    
    @pytest.fixture(scope='class', autouse=True)
    def class_setup(self):
        self.actual_resp = None
        yield

    @pytest.mark.parametrize('case', case_file_obj.positive_cases)
    def test_inland_positive(self, case):
        self.actual_resp = http_pb_simplepay(case.req_params)
        dictionary_should_contain_sub_dictionary(self.actual_resp, case.expected)


class TestInlandNegative():
    pytestmark = pytest.mark.functional, pytest.mark.regress, pytest.mark.negative
    
    @pytest.mark.parametrize('case', case_file_obj.negative_cases)
    def test_inland_negative(self, case):
        self.actual_resp = http_pb_simplepay(case.req_params)
        dictionary_should_contain_sub_dictionary(self.actual_resp, case.expected)

