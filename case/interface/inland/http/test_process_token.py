#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/17 16:19
# comment:
import pytest
from lib.common.case_processor.entry import src_case_file
from lib.interface_biz.http.process_token import get_process_token_positive

pytestmark = pytest.mark.process_token

case_file = src_case_file(__file__)


@pytest.mark.smoke
@pytest.mark.full
@pytest.mark.positive
class TestInlandPositive():

    @pytest.mark.parametrize('case', case_file.positive_cases)
    def test_inland_positive(self, case):
        result = get_process_token_positive(case)
        case_file.update_actual(case.name, result)
        assert eval(case.expected['success']) == result['success']
        if result['success'] is True:
            assert len(result['data']['processToken']) > 0
