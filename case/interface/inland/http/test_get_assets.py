'''
Created on 2021年5月25日
@author: 80319739
'''
import os
import re
import time
import pytest
from lib.common.case_processor.entry import src_case_file
from lib.common_biz.json_request import (http_encjson_request, 
                                         get_check_http_json_result_positive,
                                         get_check_http_json_result_negative)
from lib.common.utils.misc_utils import timeit
from lib.common.utils.globals import HTTPENCJSON_IN, GlobalVar
from case.interface.conftest import partner_id
from lib.interface_biz.dubbo.near_me import Nearme
from lib.common_biz.biz_db_operate import clear_all_vou
from lib.interface_biz.dubbo.vou import Voucher


HTTPENCJSON_IN.header['X-APP']['appPackage'] = 'com.oppo.usercenter'
HTTPENCJSON_IN.header['X-APP']['appVersion'] = '280'
case_file = src_case_file(__file__)
url = case_file.url
all_vou_types = 'XIAOFEI', 'DIKOU', 'DAZHE', 'XIAOFEI_DAZHE', 'RED_PACKET_COUPON'
nearme = Nearme(GlobalVar.SSOID)


@timeit
@pytest.fixture(scope='module', autouse=True)
def grant_vouchers_if_empty():
    clear_all_vou(GlobalVar.SSOID, partner_id)
    result = Voucher().query_all_useable(GlobalVar.SSOID, partner_id=partner_id)
    vouchers = result['data']
    # 判断可用的可币券类型是否包含所有
    vou_types = set(vou['couponDiscountType'] for vou in vouchers)
    if vou_types == set(all_vou_types):
        return
    else:
        voucher = Voucher()
        # 消费
        for _ in range(5):
            voucher.grant_check_voucher(partner_id, "KB_COUPON", "XIAOFEI", "0", "0.01", GlobalVar.SSOID)
        # 抵扣
        voucher.grant_check_voucher(partner_id, "KB_COUPON", "DIKOU", "1", "0.99", GlobalVar.SSOID)
        # 折扣
        voucher.grant_check_voucher(partner_id, "KB_COUPON", "DAZHE", "1", "0", GlobalVar.SSOID, ratio=0.01, maxCutAmount='1')
#         voucher.grant_check_voucher(partner_id, "KB_COUPON", "DAZHE", "1", "0", GlobalVar.SSOID, ratio=0.1, maxCutAmount='1')
        # 消费折扣
        voucher.grant_check_voucher(partner_id, "KB_COUPON", "XIAOFEI_DAZHE", "1", "0", GlobalVar.SSOID, ratio=0.01, maxCutAmount='10')
        # 红包券
        voucher.grant_check_voucher(partner_id, "KB_COUPON", "RED_PACKET_COUPON", "0", "1", GlobalVar.SSOID)


@timeit
@pytest.fixture(scope='module', autouse=True)
def add_cocoin():
    balance = nearme.query_balance()
    if balance == 0:
        nearme.nearme_add_subtract("0.02", GlobalVar.SSOID, 0)
        assert nearme.query_balance() == 0.02
        
        
@timeit
@pytest.fixture(scope='module', autouse=True, name='sheetname')
def manage_case_file():
    yield re.match('test_(\S+).py', os.path.basename(__file__), re.I).group(1)
    case_file.save()
    case_file.close()


@pytest.mark.smoke
@pytest.mark.full
@pytest.mark.positive
@pytest.mark.parametrize('case', case_file.positive_cases)
def test_inland_positive(case, sheetname):
    try:
        result = http_encjson_request(case, sheetname, url)
        get_check_http_json_result_positive(case, result)
        case.is_passed = 'passed'
    finally:
        case_file.update_req(case.name, case.req_params)
        case_file.update_actual(case.name, result)


@pytest.mark.full
@pytest.mark.negative    
@pytest.mark.parametrize('case', case_file.negative_cases)
def test_inland_negative(case, sheetname):
    try:
        result = http_encjson_request(case, sheetname, url)
        get_check_http_json_result_negative(case, result)
        case.is_passed = 'passed'
    finally:
        case_file.update_req(case.name, case.req_params)
        case_file.update_actual(case.name, result)


if __name__ == '__main__':
    argv = ['-vs', '--timeout=300', '--ff', 
#             '--cov='+os.getcwd(), '--cov-report=html', 
            r'--html=%s\report\report_%s.html' %(os.getcwd(), time.strftime('%Y-%m-%d', time.localtime())),
            __file__
           ]
    print(argv)
    pytest.main(argv)