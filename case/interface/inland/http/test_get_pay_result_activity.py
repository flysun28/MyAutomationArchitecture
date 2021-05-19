'''
Created on 2021年5月19日
@author: 80319739
'''
import pytest
from lib.common.case_processor.entry import src_case_file


case_file = src_case_file(__file__)


# @pytest.mark.smoke
# @pytest.mark.full
# @pytest.mark.positive
# class TestInlandPositive():
#  
#     @pytest.mark.parametrize('case', case_file.positive_cases)
#     def test_inland_positive(self, case):
#         result = get_marketing_info_positive(case)
#         case_file.update_actual(case.name, result)
#         assert eval(case.expected['success']) == result['success']

