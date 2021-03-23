'''
@author: 80319739
'''
import os
import time
import pytest
from lib.interface_biz.http.vip_login import Vip
from lib.common.utils.env import set_global_env_id


def pytest_configure(config):
    config.addinivalue_line('markers', 'smoke')
    config.addinivalue_line('markers', 'full')
    config.addinivalue_line('markers', 'positive')
    config.addinivalue_line('markers', 'negative')
    config.addinivalue_line('markers', 'inland')

 
# @pytest.fixture(scope='session', autouse=True)
# def global_setup_and_teardown():
#     set_global_env_id(3)
#     vip = Vip()
# #     vip.login()
#     
#     yield
#     
#     print('\nTest Finished...')


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    '''
    收集测试结果，输出到控制台
    :param terminalreporter: <_pytest.terminal.TerminalReporter object>
    :param exitstatus: e.g. ExitCode.TESTS_FAILED
    :param config: <_pytest.config.Config object>
    '''
    stats = terminalreporter.stats
    print("total:", terminalreporter._numcollected)
    for kw in 'passed', 'failed', 'error', 'skipped':
        print('%s: %d' %(kw, len(stats.get(kw, []))))    
    # terminalreporter._sessionstarttime 会话开始时间
    duration = time.time() - terminalreporter._sessionstarttime
    print('total times:', round(duration, 2), 'seconds')