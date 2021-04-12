import re
from types import ModuleType
from lib.common.session.http.protobuf import ProtoBuf
from lib.common.utils.globals import HTTPJSON_IN
from lib.common_biz.replace_parameter import ReplaceParams


def http_pb_request(case, pb_src):
    sheetname = case.ws.title
    prefix, pay_method = re.search('(simplepay_|)(\S+)', sheetname, re.I).groups()
    repl = ReplaceParams(case.req_params)
    if prefix:
        req = repl.replace_native(pay_method)
    if isinstance(pb_src, str):
        pb_module = eval(pb_src)
    elif isinstance(pb_src, ModuleType):
        pb_module = pb_src
    response = ProtoBuf(pb_module).runner(HTTPJSON_IN.prefix + '/plugin/post/simplepay', 'Request', req, flag=0)
    return response
#     result = ProtoBuf(pb_module).parser('Result', response)
#     return result

