#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/8 23:22
# comment: 国内gateway查看可币余额
from lib.common_biz.replace_parameter import replace_gateway
from lib.common.utils.globals import GlobarVar


def query_account(ssoid):
    """
    :return:
    """
    case_req = {'app_id': '100002',
                'service': 'nearme.account.query',
                'format': 'JSON',
                'charset': 'UTF8',
                'sign_type': 'MD5',
                'sign': '',
                'timestamp': '',
                'version': '1.0',
                'bizContent': str({'ssoid': '{}'.format(ssoid)})}
    replace_gateway(case_req, "100002")
    response = GlobarVar.HTTPJSON_GW_IN.post("/gateway/"+case_req['service'], data=case_req)
    # 需要确认是否加上totalGiveBalance与giveBalance
    return response['data']['useableBalance']


if __name__ == '__main__':
    query_account(GlobarVar.SSOID)