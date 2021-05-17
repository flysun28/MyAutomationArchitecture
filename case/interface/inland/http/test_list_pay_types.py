#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/17 15:52
# comment:


import pytest

from lib.common.case_processor.entry import src_case_file
from lib.interface_biz.http.list_pay_types import get_list_pay_types_positive

pytestmark = pytest.mark.list_pay_types

case_file = src_case_file(__file__)


@pytest.mark.smoke
@pytest.mark.full
@pytest.mark.positive
class TestInlandPositive():

    @pytest.mark.parametrize('case', case_file.positive_cases)
    def test_inland_positive(self, case):
        result = get_list_pay_types_positive(case)
        # 更新到实际结果对应表格中
        case_file.update_actual(case.name, result)