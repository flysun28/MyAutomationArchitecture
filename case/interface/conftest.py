'''
@author: 80319739
'''
import os
import pytest
from lib.interface_biz.http.vip_login import Vip
from lib.common.utils.env import set_global_env_id


def pytest_configure(config):
    config.addinivalue_line('markers', 'smoke')
    config.addinivalue_line('markers', 'full')
    config.addinivalue_line('markers', 'positive')
    config.addinivalue_line('markers', 'negative')
    config.addinivalue_line('markers', 'simplepay')

 
@pytest.fixture(scope='session', autouse=True)
def global_setup_and_teardown():
    '''
    1. 设置第几套测试环境
    '''
    set_global_env_id(3)
    vip = Vip()
#     vip.login()
    
    yield
    
    print('\nTest Finished...')