import re
from lib.common.session.http.protobuf import ProtoBuf
from lib.common.utils.globals import HTTPJSON_IN
from lib.common_biz.replace_parameter import ReplaceParams


def http_pb_request(case):
    sheetname = case.ws.title
    prefix, pay_procedure = re.search('(simplepay_|)(\S+)', sheetname, re.I).groups()
    repl = ReplaceParams(case.req_params)
    if prefix:
        req = repl.replace_native(pay_procedure)
    response = ProtoBuf(SimplePayPb_pb2).runner(HTTPJSON_IN.prefix + '/plugin/post/simplepay', 'Request', req, flag=0)
    result = ProtoBuf(SimplePayPb_pb2).parser('Result', response)
    return result

