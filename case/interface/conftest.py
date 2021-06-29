'''
@author: 80319739
'''
import time
import pytest
from lib.common.utils.env import set_global_env_id
from lib.common.concurrent.threading import monitor
from lib.interface_biz.http.pay_pass import get_process_token

partner_ids = '5456925', '2031'
partner_id = '2031'
env_id = '1'


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


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # 获取钩子方法的调用结果
    out = yield
    # 从钩子方法的调用结果中获取测试报告
    result = out.get_result()
    if result.when == 'call':
        case = item.funcargs.get('case')
        if case:
            if case.is_passed:
                outcome = case.is_passed
            else:
                outcome = 'failed' if monitor.obj else 'passed'
            case.file.update_running_result(case.name, outcome)
            monitor.reset(monitor.obj)
        else:
            outcome = result.outcome
#         print('测试用例%s执行报告: %s' %(item.function.__name__, result))
        print(('运行结果: %s' %outcome))
        result.outcome = outcome


@pytest.fixture(scope='session', autouse=True)
def session_setup_and_teardown():
    '''
    1. set environment id(unused)
    2. account login(unused)
    3. terminate all threads including monitor and other pytest threads, 
       otherwise python interpreter will never be stopped
    '''
    # set_global_env_id(env_id)
    from lib.interface_biz.http.user_account import Account
    
    account = Account()
#     account.login()
    
    yield
    
#     monitor.is_terminate_self = True
#     kill_all_active_threads()
    print('\nTest Finished...')


@pytest.fixture(scope='module', autouse=True)
def process_token():
    return get_process_token()
