from lib.common.utils.env import set_global_env_id
set_global_env_id(3)

from lib.common.utils.globals import HTTPENCJSON_IN
from lib.interface_biz.http.pay_pass import get_process_token
HTTPENCJSON_IN.header['X-APP']['appPackage'] = 'com.oppo.usercenter'
HTTPENCJSON_IN.header['X-APP']['appVersion'] = '280'


case_data = {
    "processToken": get_process_token(),
#     "partnerCode": "2031",
    "orderAmount": "0.02",
#     "factor": {"type":"", "resources":""},
#     "factor": '',
#     "partnerAppKey": ''
}

result = HTTPENCJSON_IN.post('/api/asset/v290/get-assets', case_data)
print(result)
