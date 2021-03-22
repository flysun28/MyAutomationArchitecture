'''
Created on 2021年3月22日
@author: 80319739
'''
import pytest
from case.scenario.inland.direct_pay import direct_pay


class TestScenarioInland():

    def test_direct_pay(self):
        direct_pay(1, 1)
