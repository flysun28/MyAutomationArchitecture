#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/17 15:45
# comment:
import os
import re
import pytest
from lib.common.case_processor.entry import src_case_file
from lib.interface_biz.http.get_marketing_info import get_marketing_info_positive

pytestmark = pytest.mark.get_marketing_info

case_file = src_case_file(__file__)

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
        result = get_marketing_info_positive(case)
        case_file.update_actual(case.name, result)
        assert eval(case.expected['success']) == result['success']