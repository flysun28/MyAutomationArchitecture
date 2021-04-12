'''
@author: 80319739
'''
import time
import pytest
from lib.common.utils.env import set_global_env_id

partner_ids = '2031', '5456925'
env_id = 3


def pytest_configure(config):
    config.addinivalue_line('markers', 'smoke')
    config.addinivalue_line('markers', 'full')
    config.addinivalue_line('markers', 'positive')
    config.addinivalue_line('markers', 'negative')
    config.addinivalue_line('markers', 'inland')
    config.addinivalue_line('markers', 'voucher')
    config.addinivalue_line('markers', 'simplepay')
    config.addinivalue_line('markers', 'pb2json')


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    '''
    收集测试结果，输出到控制台
    :param terminalreporter: <_pytest.terminal.TerminalReporter object>
    :param exitstatus: e.g. <_pytest.config.ExitCode.TESTS_FAILED>
    :param config: <_pytest.config.Config object>
    '''
    stats = terminalreporter.stats
    print("total:", terminalreporter._numcollected)
    for kw in 'passed', 'failed', 'error', 'skipped':
        print('%s: %d' %(kw, len(stats.get(kw, []))))    
    # terminalreporter._sessionstarttime 会话开始时间
    duration = time.time() - terminalreporter._sessionstarttime
    print('total times:', round(duration, 2), 'seconds')
    

@pytest.fixture(scope='session', autouse=True)
def global_setup_and_teardown():
    '''
    1. 在自动化专用数据库中保存test_account
    '''
    set_global_env_id(env_id)
    from lib.interface_biz.http.user_account import Account
    
    account = Account()
#     account.login()
    
    yield
     
    print('\nTest Finished...')


