#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/29 12:37
# comment: 海外渠道聚合接口


from lib.common.session.http.protobuf import ProtoBuf
from lib.common.utils.globals import HTTPJSON_OUT
from lib.common_biz.replace_parameter import ReplaceParams
from lib.pb_src.python_standard import PayTypes_pb2

req = {
    "header": {
        "version": "15.0",
        "token": "",
        # RSKBqSj9vK44j+/O6E3YpxS5Tr+E8xTbOAsNNA31CkTDNNY23g5M8z4C9IxrNz7/WaEQ8LZkhRx4\nDRXyyOU4AaUEudS7/+NO01gzsok2QVVLZTWz6dytdB2gazMbFGM7WKWplv2i9qTodaMvbgMLzkCg\ntnZsnHi9sim6rLRRw1k=\n
        "imei": "",
        "model": "",
        "apntype": "1",
        "package": "com.example.pay_demo",
        "r_v": "RvDf0ABC",
        "sign": "",
        "sdkVer": "4.0",
        "appVerison": "230",
        "ip": "0.0.0.0",
        # FBC4E853B36C40C8A2AC61D127D85C9E23fe8cbbef964f0009fa0ac296d07836
        "openId": "FBC4E853B36C40C8A2AC61D127D85C9E23fe8cbbef964f0009fa0ac296d07836",
        "brandType": "OPPO",
        "mobileos": "19",
        "androidVersion": "30"
    },
    "country": "IN",
    "payAmount": "1000000",
    "currency": "INR",
    "renewal": "N",
    "partnerId": "5456925",
    "factor": "",
    "isNeedAggregate": "Y",
    "noApp": "paytm_paytm",
    "callFrom": 0
}
ReplaceParams(req).replace_standard("direct")
response = ProtoBuf(PayTypes_pb2).runner(HTTPJSON_OUT.prefix + "/plugin/query/paytypes", 'PayTypesRequest', req,
                                         flag=1)
result = ProtoBuf(PayTypes_pb2).parser('PayTypesResult', response)
