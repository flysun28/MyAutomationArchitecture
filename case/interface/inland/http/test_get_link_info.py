#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/14 15:20
# comment:
import pytest
from lib.common.case_processor.entry import src_case_file
from lib.interface_biz.http.get_link_info import get_link_info_test_positive

pytestmark = pytest.mark.get_link_info

case_file = src_case_file(__file__)


@pytest.mark.smoke
@pytest.mark.full
@pytest.mark.positive
class TestInlandPositive():

    @pytest.mark.parametrize('case', case_file.positive_cases)
    def test_inland_positive(self, case):
        result = get_link_info_test_positive(case)
        # 更新到实际结果对应表格中
        case_file.update_actual(case.name, result)
        assert eval(case.expected['success']) == result['success']
        if result['success'] is True:
            if case.req_params['partnerId'] == "5456925":
                for item in result['data']['vipRights']:
                    for dict_key in item:
                        assert item[dict_key] is not None

