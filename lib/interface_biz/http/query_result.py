#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/19 9:56
# comment:
from lib.common.session.http.protobuf import ProtoBuf
from lib.common.utils.globals import HTTPJSON_IN
from lib.common_biz.replace_parameter import ReplaceParams
from lib.pb_src.python_native import QueryResultPb_pb2


def queryResult(request_id, query_type="PAY"):
    req = {
        "header": {
            "version": "5.0",
            "t_p": "",
            "imei": "",
            "model": "PBDM00",
            "apntype": "1",
            "package": "com.example.pay_demo",
            "r_v": "",
            "ext": "",
            "sdkVer": 260,
            "country": "CN",
            "currency": "CNY",
            "brandType": "OPPO",
            "mobileos": "17",
            "androidVersion": "29"
        },
        "payrequestid": request_id,
        "version": "260",
        # "queryType": "SIGN"
        "queryType": query_type
    }
    ReplaceParams(req).replace_native("expend")
    response = ProtoBuf(QueryResultPb_pb2).runner(HTTPJSON_IN.prefix + '/plugin/post/queryresult', 'Request', req, flag=0)
    result = ProtoBuf(QueryResultPb_pb2).parser('Result', response)
    return result.baseresult.code


if __name__ == '__main__':
    queryResult("KB202102231406382076075925558062")
