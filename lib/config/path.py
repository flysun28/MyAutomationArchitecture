# coding=utf-8
import os
pardir = os.path.dirname
lib_dir = project_dir = pardir(pardir(__file__))
config_dir = pardir(__file__)

log_dir = os.path.join(project_dir, 'log')

common_sql_path = os.path.join(config_dir, 'sql.ini')
global_env_path = os.path.join(config_dir, 'environment.ini')
do_case_path = os.path.join(config_dir, 'do_case.ini')
merchant_path = os.path.join(config_dir, 'merchant.ini')
