'''
Created on 2021年3月22日
@author: 80319739
'''
import pytest
from case.scenario.inland import direct_pay, no_login, only_sign, rs_only_rmb, rs_with_kb_rmb, sign_pay, spend_only_kb, spend_with_kb_vou

pytestmark = pytest.mark.inland


class TestScenarioInland():
    test_data_wo_kb = (1, 1),
    test_data_with_kb = (1, 1, 1),
    
    @pytest.mark.parametrize('amt,callback_amt', test_data_wo_kb)
    def test_direct_pay(self, amt, callback_amt):
        direct_pay(amt, callback_amt)
    
    @pytest.mark.parametrize('amt,callback_amt', test_data_wo_kb)
    def test_no_login(self, amt, callback_amt):
        no_login(amt, callback_amt)
        
    def test_only_sign(self):
        only_sign()
        
    @pytest.mark.parametrize('amt,callback_amt,kb_amt', test_data_with_kb)    
    def test_recharge_spend_rmb_and_kb(self, amt, callback_amt, kb_amt):
        '''
        默认携带了优惠券 0.01元
        '''
        rs_with_kb_rmb(amt, callback_amt, kb_amt)
    
    @pytest.mark.parametrize('amt,callback_amt', test_data_wo_kb)    
    def test_recharge_spend_only_rmb(self, amt, callback_amt):
        rs_only_rmb(amt, callback_amt)
        
    @pytest.mark.parametrize('amt,callback_amt', test_data_wo_kb)
    def test_sign_pay(self, amt, callback_amt):
        sign_pay(amt, callback_amt)
        
    @pytest.mark.parametrize('amt', (data[0] for data in test_data_wo_kb))
    def test_spend_kb_and_voucher(self, amt):
        spend_with_kb_vou(amt)
    
    @pytest.mark.parametrize('amt', (data[0] for data in test_data_wo_kb))
    def test_spend_only_kb(self, amt):
        spend_only_kb(amt)