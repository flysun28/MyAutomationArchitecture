#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/19 9:56
# comment:
from lib.common.session.http.protobuf import ProtoBuf
from lib.common.utils.globals import HTTPJSON_IN
from lib.common_biz.replace_parameter import ReplaceParams
from lib.pb_src.python_native import QueryResultPb_pb2


def queryResult(request_id, query_type="PAY", pass_type="expend"):
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
            "sdkVer": 265,
            "country": "CN",
            "currency": "CNY",
            "brandType": "OPPO",
            "mobileos": "17",
            "androidVersion": "29"
        },
        "payrequestid": request_id,
        "version": "265",
        # "queryType": "SIGN"
        "queryType": query_type
    }
    # 鉴权，获取t_p、r_v更新到req中
    ReplaceParams(req).replace_native(pass_type)
    pb = ProtoBuf(QueryResultPb_pb2)
    response = pb.runner(HTTPJSON_IN.prefix + '/plugin/post/queryresult', 'Request', req, flag=0)
    result = pb.parser('Result', response)
    return str(result.baseresult.code)


if __name__ == '__main__':
    queryResult("KB202107151525122086776969116272")
