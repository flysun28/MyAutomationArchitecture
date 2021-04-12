# coding=utf-8

import os
import re
from lib.config.path import global_env_path, config_dir
from lib.common.file_operation.config_operation import Config

glob_env_cfg = Config(global_env_path)


def set_global_env_id(env_id):
    if isinstance(env_id, int):
        env_id = str(env_id)
    elif not env_id.isdigit():
        env_id = re.search('[a-zA-Z]+$', env_id).group()
    glob_env_cfg.write_config('environment', 'value', env_id)
    assert glob_env_cfg.read_config('environment', 'value') == env_id


def get_env_id():
    # 默认走itest平台环境变量，若无，则读取本地环境变量
    env = dict(os.environ)
    print('所有环境变量:', env)
    env_id = env.get('CASE_ENV')
    if env_id:
        set_global_env_id(env_id)
        return str(env_id)
    else:
        return glob_env_cfg.read_config('environment', 'value')


def get_env_config() -> dict:
    env_id = get_env_id()
    env_config_path = os.path.join(config_dir, 'test_env_config_%s.ini' % env_id)
    env_config = Config(env_config_path)
    result = {}
    for section in env_config.sections():
        result[section] = env_config.as_dict(section)
    # 账号域名
    account_urls = glob_env_cfg.as_dict('account_url')
    result['account_url'] = account_urls['test'] if env_id.isdigit() else account_urls['bj_sm']
    return result


def get_dubbo_info(dubbo_config, in_out="inland") -> list:
    """
    根据配置文件，返回dubbo接口的ip：port
    :param in_out:
    :param dubbo_config: test_env_config_x.ini文件中dubbo对应的服务
    :return: [ip, port]
    """
    ip_port = get_env_config()['dubbo_' + in_out][dubbo_config].split(":")
    return ip_port




if __name__ == '__main__':
    set_global_env_id("1")
