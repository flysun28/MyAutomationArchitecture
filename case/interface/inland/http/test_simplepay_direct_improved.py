'''
@author: 80319739
'''
import os
import time
import pytest
from lib.common.session.http.protobuf import ProtoBuf
from lib.common_biz.pbjson import pb2json, pb2dict
from lib.common.utils.misc_utils import dictionary_should_contain_sub_dictionary, flatten_nested_dict
from lib.common_biz.pb_request import http_pb_request
from lib.pb_src.python_native import SimplePayPb_pb2
from case.interface.inland.http.conftest import src_case_file
if __name__ == '__main__':
    from lib import pardir
    os.getcwd = lambda: pardir(pardir(pardir(pardir(__file__))))

pytestmark = pytest.mark.simplepay


def case_file():
    return src_case_file(__file__)


@pytest.mark.smoke
@pytest.mark.full
@pytest.mark.positive
class TestInlandPositive():
    
    @pytest.mark.parametrize('case', case_file().positive_cases)
    def test_inland_positive(self, case):
        response = http_pb_request(case, SimplePayPb_pb2)
        assert response.status_code == case.status_code
        result = ProtoBuf(SimplePayPb_pb2).parser('Result', response)
        # 更新到实际结果对应表格中，必须为字符串
        case_file.update_actual(case.name, pb2json(result))
        # 转字典，方便比较
        actual_result = pb2dict(result)
        res4check = flatten_nested_dict(actual_result)
        dictionary_should_contain_sub_dictionary(res4check, case.expected)
    

@pytest.mark.full
@pytest.mark.negative
class TestInlandNegative():
    
    def test_inland_negative(self, case_file):
        for case in case_file.positive_cases:
            self.actual_result = http_pb_request(case, SimplePayPb_pb2)
            dictionary_should_contain_sub_dictionary(self.actual_result, case.expected)


if __name__ == '__main__':
    argv = ['-vs', '-m', 'positive', '--timeout=300', #'--ff', 
            '--cov='+os.getcwd(), '--cov-report=html', 
            r'--html=%s\report\report_%s.html' %(os.getcwd(), time.strftime('%Y-%m-%d', time.localtime())),
            __file__
           ]
    print(argv)
    pytest.main(argv)
    

