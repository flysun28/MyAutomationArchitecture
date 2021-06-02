#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/5/14 15:20
# comment:
import time
import os
import re
import pytest
from lib.common.case_processor.entry import src_case_file
from lib.common.file_operation.config_operation import Config
from lib.common.utils.globals import GlobalVar
from lib.config.path import common_sql_path
from lib.interface_biz.http.get_link_info import get_link_info_test_positive

pytestmark = pytest.mark.get_link_info

case_file = src_case_file(__file__)

@pytest.fixture(scope='module', autouse=True, name='sheetname')
def manage_case_file():
    yield re.match('test_(\S+).py', os.path.basename(__file__), re.I).group(1)
    case_file.save()
    case_file.close()
    
mysql = GlobalVar.MYSQL_IN

@pytest.mark.smoke
@pytest.mark.full
@pytest.mark.positive
class TestInlandPositive():

    @pytest.mark.parametrize('case', case_file.positive_cases)
    def test_inland_positive(self, case):
        result = get_link_info_test_positive(case)
        case_file.update_actual(case.name, result)
        assert eval(case.expected['success']) == result['success']
        if result['success'] is True:
            if case.req_params['partnerId'] == "5456925":
                for item in result['data']['vipRights']:
                    for dict_key in item:
                        assert item[dict_key] is not None
                    sql_partner_vip_info = str(Config(common_sql_path).read_config("pay_baseshop", "partner_vip_info"))\
                        .format(time.strftime("%Y-%m-%d %H:%M:%S"), time.strftime("%Y-%m-%d %H:%M:%S"), case.req_params['partnerId'])
                    partner_vip_info = mysql.select_one(sql_partner_vip_info)
                    assert partner_vip_info['img_url'] == result['data']['vipRights'][0]['imgUrl']
                    assert partner_vip_info['redirect_url'] == result['data']['vipRights'][0]['redirectUrl']

