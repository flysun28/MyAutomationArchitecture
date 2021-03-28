# coding=utf-8


'''
Created on 2021年2月9日
@author: 80319739
'''
import os
import sys
from lib.common.session.http.http_json import HttpJsonSession
from lib.common.utils.env import get_env_config, get_env_id, set_global_env_id
from lib.common.db_operation.mysql_operation import connect_mysql, connect_auto_test_special
from lib.common.db_operation.redis_operation import connect_redis
from lib.common.utils.descriptors import GlobalVarDescriptor
from lib.config.path import do_case_path, common_sql_path, global_env_path, case_dir
from lib.common.file_operation.config_operation import Config

 
class GlobalVar():
    env_id = get_env_id()
    ENV_CONFIG = get_env_config()
    print(env_id, ENV_CONFIG)
    URL_PAY_IN = ENV_CONFIG['url']['pay_in']
    URL_PAY_OUT = ENV_CONFIG['url']['pay_out']
    URL_GW_IN = ENV_CONFIG['url']['pay_gateway_in']
    URL_GW_OUT = ENV_CONFIG['url']['pay_gateway_out']
    URL_PAY_SCARLETT = ENV_CONFIG['url']['pay_scarlet']
    HTTPJSON_IN = GlobalVarDescriptor(HttpJsonSession(URL_PAY_IN))
    HTTPJSON_OUT = GlobalVarDescriptor(HttpJsonSession(URL_PAY_OUT))
    HTTPJSON_GW_IN = GlobalVarDescriptor(HttpJsonSession(URL_GW_IN))
    HTTPJSON_GW_OUT = GlobalVarDescriptor(HttpJsonSession(URL_GW_OUT))
    HTTPJSON_SCARLET = GlobalVarDescriptor(HttpJsonSession(URL_PAY_SCARLETT))
    MYSQL_IN = GlobalVarDescriptor(connect_mysql())
    if env_id != '2':
        MYSQL_OUT = GlobalVarDescriptor(connect_mysql('oversea'))
        REDIS_IN = GlobalVarDescriptor(connect_redis())
        REDIS_OUT = GlobalVarDescriptor(connect_redis('oversea'))
    SDK_VER_IN = Config(do_case_path).read_config("sdk_ver", "version")
    SDK_VER_OUT = Config(do_case_path).read_config("apk_ver_oversea", "version")

    MYSQL_AUTO_TEST = connect_auto_test_special()
    
    sql_test_account = ""
    if env_id == "1" or env_id == "2" or env_id == "3":
        # SELECT * FROM `pay_auto_test_info`.`test_env_account` WHERE username = '{}'
        sql_test_account = Config(common_sql_path).read_config("pay_auto_test_info", "test_select_account").\
            format(Config(global_env_path).read_config("test_count", "count"))
    if env_id == "grey" or env_id == "product":
        sql_test_account = Config(common_sql_path).read_config("pay_auto_test_info", "product_select_account").\
            format(Config(global_env_path).read_config("test_count", "count"))
    TEST_ACCOUNT = MYSQL_AUTO_TEST.select_one(sql_test_account)
    if env_id == "1" or env_id == "2" or env_id == "3":
        SSOID = TEST_ACCOUNT['ssoid']
        TOKEN = TEST_ACCOUNT['token']    

HTTPJSON_IN = GlobalVar.HTTPJSON_IN
HTTPJSON_OUT = GlobalVar.HTTPJSON_OUT
if GlobalVar.env_id != '2':
    redis = REDIS = GlobalVar.REDIS_IN
HTTPJSON_SCARLET = GlobalVar.HTTPJSON_SCARLET
MYSQL_AUTO_TEST = GlobalVar.MYSQL_AUTO_TEST
CASE_SRCFILE_ROOTDIR = os.path.join(case_dir, 'src')




