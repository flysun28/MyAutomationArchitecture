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
        env_id = re.search('\d+', env_id).group()
    glob_env_cfg.write_config('environment', 'value', env_id)
    assert glob_env_cfg.read_config('environment', 'value') == env_id


def get_env_id():
    return glob_env_cfg.read_config('environment', 'value')


def get_env_config() -> dict:
    env_id = get_env_id()
    env_config_path = os.path.join(config_dir, 'test_env_config_%s.ini' % env_id)
    env_config = Config(env_config_path)
    result = {}
    for section in env_config.sections():
        result[section] = env_config.as_dict(section)
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
    pass
