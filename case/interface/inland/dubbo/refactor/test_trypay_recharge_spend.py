'''
@author: 80319739
'''
import os
import time
import pytest
import random
from lib.common.case_processor.entry import src_case_file
from lib.interface_biz.dubbo.refactor.paycenter import create_payorder_positive, create_payorder_negative
from lib.interface_biz.http.grant_voucher import HttpGrantSingleVous
from case.interface.conftest import partner_ids
from lib.interface_biz.dubbo.near_me import Nearme
from lib.common.utils.globals import GlobalVar
from lib.interface_biz.dubbo.vou import Voucher


if __name__ == '__main__':
    from lib import pardir
    os.getcwd = lambda: pardir(pardir(pardir(pardir(__file__))))

# 从测试专用数据库中随机获取ssoid
partner_id = random.choice(partner_ids)

case_file = src_case_file(__file__)
# 计算带券的测试用例数，发放对应数量的可币券
vou_count = len([1 for tc in case_file.all_cases if tc.voucherInfo and tc.type == '+'])
# 计算带可币的测试用例数，增加对应数量的可币
cocoin_num = round(sum([float(tc.kebiSpent) for tc in case_file.all_cases], 0), 2)


@pytest.fixture(scope='module', autouse=True)
def manage_case_file():
    yield
    case_file.save()
    case_file.close()


@pytest.fixture(scope='module', autouse=True, name='voucher_ids')
def grant_voucher_if_needed():
    '''
    1. 根据当前表格中的测试数据voucherInfo，计算需要消费的券数目，并发放。券类型、金额均随机
    2. dubbo查券信息
    3. 将券id、面额，更新至测试数据voucherInfo（内存）
    '''    
    vou_type = random.choice([1, 2, 5, 7, 8])
    httpobj = HttpGrantSingleVous(vou_type, partner_id=partner_id)
    vouids = httpobj.post(count=vou_count)
    cp_vouids = vouids.copy()
    voucher = Voucher('inland')
    for tc in case_file.all_cases:
        if tc.voucherInfo and cp_vouids:
            vouid = random.choice(cp_vouids)
            tc.voucherInfo['vouId'] = vouid
            cp_vouids.remove(vouid)
            vou_info = voucher.query_voucher_by_id(GlobalVar.SSOID, vouid)
            tc.voucherInfo['price'] = vou_info['data']['originalAmount'] or vou_info['data']['maxCutAmount']
            case_file.update_voucher_info(tc.name, tc.voucherInfo)
#     print(voucher.query_all_useable(GlobalVar.SSOID))
    yield vouids


@pytest.fixture(scope='module', autouse=True)
def add_cocoin():
    '''
    1. 查询当前可币余额
    2. 若小于当前表格测试数据所需可币总额，则dubbo发放可币
    '''
    nearme = Nearme(ssoid=GlobalVar.SSOID)
    current_balance = nearme.query_balance()
    if float(current_balance) < cocoin_num:
        nearme.nearme_add_subtract_wo_ssoid(cocoin_num, 0)
        updated_balance = nearme.query_balance()
        assert updated_balance == current_balance + cocoin_num, \
                '{} != {} + {}'.format(updated_balance, current_balance, cocoin_num)


@pytest.mark.smoke
@pytest.mark.full
@pytest.mark.positive
@pytest.mark.parametrize('case', case_file.positive_cases)
def test_create_recharge_spend_pay_positive(case):
    try:
        req, result = create_payorder_positive(case, partner_id=partner_id)
    finally:
        # 更新下发请求报文体到对应表格中
        case_file.update_req(case.name, req)
        # 更新到实际结果对应表格中
        case_file.update_actual(case.name, result)


@pytest.mark.full
@pytest.mark.negative
@pytest.mark.parametrize('case', case_file.negative_cases)
def test_create_recharge_spend_pay_negative(case, expect_error=True):
    try:
        req, result = create_payorder_negative(case, partner_id=partner_id)
    finally:
        # 更新下发请求报文体到对应表格中
        case_file.update_req(case.name, req)
        # 更新到实际结果对应表格中
        case_file.update_actual(case.name, result)
    


if __name__ == '__main__':
    argv = ['-vs', '-m', 'negative ', '--timeout=300', '--ff', 
#             '--cov='+os.getcwd(), '--cov-report=html', 
            r'--html=%s\report\report_%s.html' %(os.getcwd(), time.strftime('%Y-%m-%d', time.localtime())),
            __file__
           ]
    print(argv)
    pytest.main(argv)
