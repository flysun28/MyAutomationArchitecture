'''
Created on 2021年3月29日
@author: 80319739
'''
import os
import pytest
import random
import string
import time
from itertools import chain
from concurrent.futures import ALL_COMPLETED, wait
from concurrent.futures.thread import ThreadPoolExecutor
from lib.common.utils.misc_utils import create_random_str, extend_to_longest
from lib.common_biz.find_database_table import SeparateDbTable
from case.interface.conftest import partner_ids
from lib.interface_biz.http.grant_voucher import VouInfo, HttpGrantMultiVous, HttpGrantSingleVous
from lib.common.exception.intf_exception import IgnoreException
from lib.common.utils.globals import CASE_SRCFILE_ROOTDIR, GlobalVar
from lib.interface_biz.http.user_account import Account

pytestmark = pytest.mark.voucher

case_file_path = os.path.join(CASE_SRCFILE_ROOTDIR, 'http', 'inland.xlsx')
vouinfo = VouInfo(case_file_path)
vouinfo.create()


@pytest.fixture(scope='module', autouse=True)
def ssoids():
    acc = Account()
    acc.get_all_ssoids()
    return acc.all_test_ssoids


class TestMultiVou():
   
    @pytest.fixture(scope='class', autouse=True)
    def httpobj(self, ssoids):
        ssoid = random.choice(ssoids)
        partner_id = random.choice(partner_ids)
        yield HttpGrantMultiVous(vouinfo, ssoid, partner_id)
    
    @pytest.mark.positive
    def test_positive(self, httpobj):
        # 批量发券正常测试
        httpobj.post()    


class TestSingleVou():
    
    @pytest.fixture(scope='class', autouse=True)
    def httpobj(self, ssoids):
        ssoid = random.choice(ssoids)
        partner_id = random.choice(partner_ids)
        yield HttpGrantSingleVous(ssoid, partner_id)
        
    @pytest.mark.positive
    def test_positive(self, httpobj):
        # 批量发券正常测试
        httpobj.post()    

