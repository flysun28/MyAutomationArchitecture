# coding=utf-8

import os
import re
from config.path import global_env_path, config_dir
from common.file_operation.config_operation import Config


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
