'''
Created on 2021年3月22日
@author: 80319739
'''
import pytest
from case.scenario.overseas import kb_spend, kb_vou_spend, recharge, rs_only_channel, rs_with_vou_channel, skip_pay, skip_pay_no_login


class TestScenarioOverseas():
    test_data_wo_kb = (1000, 1000),
    
    @pytest.mark.parametrize('amt,callback_amt', test_data_wo_kb)
    def test_no_login(self, amt, callback_amt):
        skip_pay_no_login(amt, callback_amt)
        
    @pytest.mark.parametrize('amt,callback_amt', test_data_wo_kb)    
    def test_recharge_spend_only_rmb(self, amt, callback_amt):
        rs_only_channel(amt, callback_amt)
    
    @pytest.mark.parametrize('amt,callback_amt', test_data_wo_kb)
    def test_recharge_spend_rmb_and_kb(self, amt, callback_amt):
        rs_with_vou_channel(amt, callback_amt)
        
    @pytest.mark.parametrize('amt,callback_amt', test_data_wo_kb)
    def test_recharge(self, amt, callback_amt):
        recharge(amt, callback_amt)
        
    @pytest.mark.parametrize('amt,callback_amt', test_data_wo_kb)
    def test_skip_pay(self, amt, callback_amt):
        skip_pay(amt, callback_amt)
        
    @pytest.mark.parametrize('amt', (data[0] for data in test_data_wo_kb))
    def test_spend_kb_and_voucher(self, amt):
        kb_vou_spend(amt)
    
    @pytest.mark.parametrize('amt', (data[0] for data in test_data_wo_kb))
    def test_spend_only_kb(self, amt):
        kb_spend(amt)
    
