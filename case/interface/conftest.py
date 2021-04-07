'''
@author: 80319739
'''
import pytest

partner_ids = '2031', '5456925'


def pytest_configure(config):
    config.addinivalue_line('markers', 'smoke')
    config.addinivalue_line('markers', 'full')
    config.addinivalue_line('markers', 'positive')
    config.addinivalue_line('markers', 'negative')
    config.addinivalue_line('markers', 'inland')
    config.addinivalue_line('markers', 'voucher')
    config.addinivalue_line('markers', 'simplepay')
    config.addinivalue_line('markers', 'pb2json')


@pytest.fixture(scope='session', autouse=True)
def global_setup_and_teardown():
    '''
    1. 根据在自动化专用数据库中保存的test_account
    '''
    
    from lib.interface_biz.http.user_account import Account
    
    account = Account()
#     account.login()
    
    yield
     
    print('\nTest Finished...')
