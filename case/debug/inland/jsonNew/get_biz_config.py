from lib.common.utils.env import set_global_env_id
set_global_env_id(3)

from lib.common.utils.globals import HTTPENCJSON_IN
# HTTPENCJSON_IN.header['X-APP']['appPackage'] = 'com.oppo.usercenter'
# HTTPENCJSON_IN.header['X-APP']['appVersion'] = '280'


case_data = {
    'partnerCode': '2031'
}

result = HTTPENCJSON_IN.post('/api/conf/v290/get-biz-config', case_data)
