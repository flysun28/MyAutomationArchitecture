'''
@author: 80319739
'''
import os
import time
import pytest
import random
from lib.common.case_processor.entry import src_case_file
from case.interface.conftest import partner_ids
from lib.interface_biz.dubbo.refactor.paycenter import create_payorder_positive, create_payorder_negative

if __name__ == '__main__':
    from lib import pardir
    os.getcwd = lambda: pardir(pardir(pardir(pardir(__file__))))

pytestmark = pytest.mark.simplepay

# 从测试专用数据库中随机获取ssoid
partner_id = random.choice(partner_ids)

case_file = src_case_file(__file__)


@pytest.fixture(scope='module', autouse=True)
def manage_case_file():
    yield
    case_file.save()
    case_file.close()


@pytest.mark.smoke
@pytest.mark.full
@pytest.mark.positive
@pytest.mark.parametrize('case', case_file.positive_cases)
def test_create_kb_recharge_positive(case):
    try:
        req, result = create_payorder_positive(case, partner_id=partner_id, partner_order='')
    finally:
        # 更新下发请求报文体到对应表格中
        case_file.update_req(case.name, req)
        # 更新到实际结果对应表格中
        case_file.update_actual(case.name, result)


@pytest.mark.full
@pytest.mark.negative
@pytest.mark.parametrize('case', case_file.negative_cases)
def test_create_kb_recharge_negative(case):
    try:
        req, result = create_payorder_negative(case, partner_id=partner_id, partner_order='')
    finally:
        # 更新下发请求报文体到对应表格中
        case_file.update_req(case.name, req)
        # 更新到实际结果对应表格中
        case_file.update_actual(case.name, result)


if __name__ == '__main__':
    argv = ['-vs', '-m', 'positive or negative', '--timeout=300', '--ff', 
#             '--cov='+os.getcwd(), '--cov-report=html', 
            r'--html=%s\report\report_%s.html' %(os.getcwd(), time.strftime('%Y-%m-%d', time.localtime())),
            __file__
           ]
    print(argv)
    pytest.main(argv)
