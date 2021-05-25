'''
@author: 80319739
'''
import time
import pytest
from lib.common.utils.env import set_global_env_id
from lib.common.concurrent.threading import monitor

env_id = 1


def pytest_configure(config):
    config.addinivalue_line('markers', 'smoke')
    config.addinivalue_line('markers', 'full')
    config.addinivalue_line('markers', 'positive')
    config.addinivalue_line('markers', 'negative')
    config.addinivalue_line('markers', 'inland')


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
    
    
@pytest.fixture(scope='session', autouse=True)
def session_setup_and_teardown():
    '''
    1. set environment id(unused)
    2. account login(unused)
    3. terminate all threads including monitor and other pytest threads, 
       otherwise python interpreter will never be stopped
    '''
    set_global_env_id(env_id)
   
    yield
    
    monitor.is_terminate_self = True
    print('\nTest Finished...')