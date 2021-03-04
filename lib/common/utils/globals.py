# coding=utf-8


'''
Created on 2021年2月9日
@author: 80319739
'''
import os
from lib.common.session.http.http_json import HttpJsonSession
from lib.common.utils.env import get_env_config
from lib.common.db_operation.mysql_operation import connect_mysql
from lib.common.db_operation.redis_operation import connect_redis
from lib.common.utils.descriptors import GlobalVarDescriptor
from lib.config.path import test_account_path, do_case_path
from lib.common.file_operation.config_operation import Config


class GlobarVar():
    ENV_CONFIG = get_env_config()
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
    MYSQL_OUT = GlobalVarDescriptor(connect_mysql('oversea'))
    REDIS_IN = GlobalVarDescriptor(connect_redis())
    REDIS_OUT = GlobalVarDescriptor(connect_redis('oversea'))
    SSOID = Config(test_account_path).read_config("account", "ssoid")
    SDK_VER_IN = Config(do_case_path).read_config("sdk_ver", "version")
    SDK_VER_OUT = Config(do_case_path).read_config("apk_ver_oversea", "version")


HTTPJSON_IN = GlobarVar.HTTPJSON_IN
HTTPJSON_OUT = GlobarVar.HTTPJSON_OUT
redis = REDIS = GlobarVar.REDIS_IN
HTTPJSON_SCARLET = GlobarVar.HTTPJSON_SCARLET
CASE_SRCFILE_ROOTDIR = os.path.join(os.getcwd(), 'src')
