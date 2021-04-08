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
    
    @pytest.mark.negative
    def test_outer_params_negative(self, httpobj):
        # 批量发券异常测试
        ########################################### 外层参数负向测试 Start ###########################################
        '异常测试受限：长度越界会自动截断，非str会转换为str类型'
        rand_str_65 = ''.join(random.sample(string.ascii_letters+string.digits, 33))*2
        ssoids = httpobj.ssoid, '', #rand_str_65
        countries = 'CN', '',  #rand_str_65
        timezones = 'GMT+08:00', '', #rand_str_65
        currencies = 'CNY', '', #rand_str_65
        appids = httpobj.partner_id, '', #rand_str_65
        partner_orders = create_random_str(62), '', rand_str_65
        ########################################### 外层参数负向测试 End   ###########################################
        httpobj.common_params_negative_test(ssoid=ssoids,
                                            country=countries,
                                            timezone=timezones,
                                            currency=currencies,
                                            appId=appids,
                                            requestId=partner_orders)
    
    @pytest.mark.negative
    def test_vouinfolist_negative(self, httpobj):
        ########################################### 内层参数负向测试 Start ###########################################
        voutypes = '1', 5*'a', -1000
        names = 'CN', '', -1.234
        grantCounts = 1, 0
        amounts = 1.234, '', 5*'a', 9999999999.999
        maxAmounts = 9999999999.99, '2031', '', -1.234, 9999999999.999, 10000000000
        ratios = 0.999, 10000000000, '', -1.234
        beginTimes = 1, 2**32+1, ''
        expireTimes = 1, 0, 2**32+1, ''
        scopeIds = 'a', ''
        subScopeIds = '',
        blackScopeIds = 'b',
        settleTypes = 1, -1, 'a', ''
        batchIds = 'a', 0, ''
        ########################################### 内层参数负向测试 End   ###########################################
        httpobj.vouinfolist_negative_test(vouType=voutypes,
                                          vouName=names,
                                          grantCount=grantCounts,
                                          amount=amounts,
                                          maxAmount=maxAmounts,
                                          ratio=ratios,
                                          beginTime=beginTimes,
                                          expireTime=expireTimes,
                                          scopeId=scopeIds,
                                          subScopeId=subScopeIds,
                                          blackScopeId=blackScopeIds,
                                          settleType=settleTypes,
                                          batchId=batchIds)
        
    @pytest.mark.performance
    @pytest.mark.parametrize('tps', [500, 2000])
    def test_performance(self, tps, ssoids):
        all_request_ids = {}
        all_tasks = []
        thr_num = int(tps/len(ssoids))
        executor = ThreadPoolExecutor(max_workers=thr_num)
        for ssoid in ssoids:
            httpobj = HttpGrantMultiVous(vouinfo, ssoid, '2031')
            start = time.perf_counter()
            [all_tasks.append(executor.submit(httpobj.post))
                              for i in range(executor._max_workers)]
            while time.perf_counter() - start < 10:
                # 为防止submit中启动线程速度过快，而导致request_ids并未获取到，加此循环校验等待
                if len(httpobj.request_ids) < executor._max_workers:
                    time.sleep(0.5)
                else:
                    break
            else:
                print('实际发送请求数: %d\t期望发送请求数: %d' %(len(httpobj.request_ids), executor._max_workers))
                raise Exception('Exceed 10s, TIMEOUT!')
            for reqid in httpobj.request_ids:
                all_request_ids.setdefault(ssoid, set()).add(reqid)
        wait(all_tasks, return_when=ALL_COMPLETED)
#         exp_vou_count = httpobj.vouinfo_obj.count * executor._max_workers
#         for ssoid in ssoids:
#             table_id = SeparateDbTable(ssoid).get_vou_table()
#             sql = "SELECT COUNT(id) FROM oppopay_voucher.vou_info_%d WHERE ssoid='%s' AND createTime >= CURRENT_TIMESTAMP - INTERVAL 2 MINUTE ORDER BY id DESC;" %(table_id, ssoid)
#             count = GlobalVar.MYSQL_IN.select_one(sql)['COUNT(id)']
#             with IgnoreException(None) as _:
#                 assert count == exp_vou_count, \
#                     'The incremental number of oppopay_voucher.vou_info_%d: %d != %d' %(table_id, count, exp_vou_count)
#             sql = "SELECT partnerOrder FROM oppopay_voucher.vou_info_%d WHERE ssoid='%s' AND createTime >= CURRENT_TIMESTAMP - INTERVAL 2 MINUTE ORDER BY id DESC;" %(table_id, ssoid)
#             db_request_ids = set(chain(*(d.values() for d in GlobalVar.MYSQL_IN.select(sql))))
#             for reqid in all_request_ids[ssoid]:
#                 with IgnoreException(None) as _:
#                     assert reqid in db_request_ids, 'requestId %s not in oppopay_voucher.vou_info_%d' %(reqid, table_id)


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
    
    @pytest.mark.negative
    def test_negative(self, httpobj):
        ########################################### 单张发券异常测试 Start ###########################################
        '异常测试受限：长度越界会自动截断，非str会转换为str类型'
#         rand_str_65 = ''.join(random.sample(string.ascii_letters+string.digits, 33))*2
        ssoids = httpobj.ssoid, '', #rand_str_65
        amounts = 100, '', -1, 9999999999.999, 10000000000
        maxAmounts = 1000, '', -1, 9999999999.999, 10000000000
        appIds = '5456925', 65*'a', 
        appSubNames = 'a', 1
        blackScopeIds = '', 1
        checkNames = 'yf', '', 1
        configIds = '', 1
        counts = 1, 0, '', 'a'
        countries = 'CN', 1
        currencies = 'CNY', 1
        expireTimes = 'a', '', 1
        ext1 = '', 1
        ext2 = '', 1
        names = 'a', 1
        partnerOrders = 'a', 1, 65*'a'
        ratios = 0.1, 0, 'a'
        remarks = '', 1
        salePrices = 100, '', -1, 9999999999.999, 10000000000
        scopeIds = 'a', 1, ''
        settleTypes = 0, '', 'aaa'
        subScopeIds = '', 1
        timezones = '', 1
        types = 1, 0, ''
        useableTimes = '2021-01-01 00:00:00', '', 1
        ########################################### 单张发券异常测试 End   ###########################################
        httpobj.common_params_negative_test(ssoid=ssoids,
                                            country=countries,
                                            timezone=timezones,
                                            currency=currencies,
                                            appId=appIds,
                                            partnerOrder=partnerOrders,
                                            amount=amounts,
                                            maxAmount=maxAmounts,
                                            count=counts,
                                            appSubName=appSubNames,
                                            blackScopeId=blackScopeIds,
                                            checkName=checkNames,
                                            configId=configIds,
                                            expireTime=expireTimes,
                                            ext1=ext1,
                                            ext2=ext2,
                                            name=names,
                                            ratio=ratios,
                                            remark=remarks,
                                            salePrice=salePrices,
                                            scopeId=scopeIds,
                                            settleType=settleTypes,
                                            subScopeId=subScopeIds,
                                            type=types,
                                            useableTime=useableTimes)
        
    @pytest.mark.performance
    @pytest.mark.parametrize('tps', [500, 900])
    def test_performance(self, tps, ssoids):
        all_tasks = []
        thr_num = int(tps/len(ssoids))
        executor = ThreadPoolExecutor(max_workers=thr_num)
        vou_types = [1, 2, 5, 7, 8]
        random.shuffle(vou_types)
        for ssoid, voutype in zip(*extend_to_longest([ssoids, vou_types])):
            httpobj = HttpGrantSingleVous(voutype, ssoid, partner_id='2031')
            [all_tasks.append(executor.submit(httpobj.post))
                              for i in range(executor._max_workers)]
        wait(all_tasks, return_when=ALL_COMPLETED)

