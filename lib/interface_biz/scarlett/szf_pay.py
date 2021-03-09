#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/4 11:50
# comment:
import requests
from lib.common.algorithm.md5 import md5
from lib.common.utils.env import get_env_config, set_global_env_id
from lib.common_biz.sign import szf_pay_sign_string


def szf_pay(pay_req_id, card_amount, pay_money):
    """
    {payResult=1,
    privateField=testfield,
    returnMd5Str=b6b17ec2372b80eb48473a141edfe197,
    orderId=KB202103040028480281832542074350,
    payDetails=,
    cardMoney=10000,
    paymoney=10000,
    merId=164928,
    signstr=AH+8btQ2BNjuVxpHPBkpk6TitzgamfP5MFGLdZ9YIEDNNaNz0ux0T6rD+6hcLqNGbLLtFh0FcjtphTbacqPFRN5C30WWtiEgxzuMmKMl/u4QcVyLHVgEZsQDMsQy5mAtpb/DDTBFU8hb8LHdi/f7QBBIi+OeByHfNgTM5Rn3b6c=,
    version=3,
    errorcode=200}
    :return:
    """
    szf_scarlett = {
        "payResult": "1",
        "privateField": "testfield",
        "md5String": "",
        "orderId": pay_req_id,
        "payDetails": "",
        # 分
        "cardMoney": card_amount,
        "payMoney": pay_money,
        "merId": "164928",
        "signString": "bujiaoyan",
        "version": "3",
        "errcode": "200"
    }
    szf_scarlett['md5String'] = md5(szf_pay_sign_string(szf_scarlett) + "azkypmyzip82sx9tynmoqlsxcvt653yu", to_upper=False)
    response = requests.post(get_env_config()['url']['pay_scarlet'] + "/opaycenter/szfnotify",
                             data=szf_scarlett)
    print(response.content)


if __name__ == '__main__':
    set_global_env_id(3)
    szf_pay("KB202103091444452086100900255582", "100000", "100000")

