# coding=utf-8
import os
pardir = os.path.dirname
project_dir = pardir(pardir(__file__))
config_dir = pardir(__file__)

log_dir = os.path.join(project_dir, 'log')

common_sql_path = os.path.join(config_dir, 'sql.ini')
global_env_path = os.path.join(config_dir, 'environment.ini')
