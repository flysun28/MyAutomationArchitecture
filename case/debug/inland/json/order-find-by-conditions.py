import time

from lib.common.algorithm.md5 import md5
from lib.common.utils.globals import GlobalVar
from lib.common_biz.find_key import GetKey
from lib.common_biz.sign import Sign

app_id = "100001"

service = "order-find-by-conditions"


data = {"app_id": app_id,
        "service": service,
        "format": "JSON",
        "charset": "utf8",
        "sign_type": "MD5",
        "sign": "",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "version": "1.0",
        "bizContent": '{"ssoid":"2076075925","page":0,"size": 100}'
        }
temp_string = Sign(data).join_asc_have_key("") + GetKey(data['app_id']).get_key_from_server_info()
data['sign'] = md5(temp_string)
GlobalVar.HTTPJSON_GW_IN.post("/gateway/" + service, data=data)
