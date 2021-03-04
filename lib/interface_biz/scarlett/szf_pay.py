#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/4 11:50
# comment:

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

{payResult=1,
privateField=testfield,
returnMd5Str=f574e291d0f9686040b4fafaab266c5c,
orderId=KB202103030007290386082584367620,
payDetails=,
cardMoney=3000,
paymoney=3000,
merId=164928,
signstr=Jc/10tHzsyjAjLnL7cOuMEA0jy0dQZr//AKhPfrffgYuMA4S6PCZFUPV85jJ4nyP9rF3Ai5B4b0yzluaUvZVQ6R8nrQm+DY+j1iWT6Lk9q8WpkMVO0SlsW9ArttMRs35foOjM8foT8HNQKPiDs2NjUJFUJOtJlps22czjTBBEG0=,
version=3,
errorcode=200}

"""
import requests
from lib.common.algorithm.md5 import md5
from lib.common.utils.env import get_env_config
from lib.common_biz.sign import szf_pay_sign_string


def szf_pay(pay_req_id, card_amount, pay_money):
    """
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
    print(szf_pay_sign_string(szf_scarlett) + "azkypmyzip82sx9tynmoqlsxcvt653yu")
    szf_scarlett['md5String'] = md5(szf_pay_sign_string(szf_scarlett) + "azkypmyzip82sx9tynmoqlsxcvt653yu", to_upper=False)
    print(szf_scarlett)
    response = requests.post(get_env_config()['url']['pay_scarlet'] + "/opaycenter/szfnotify",
                             data=szf_scarlett)
    print(response.content)


if __name__ == '__main__':
    szf_pay("KB202103041512202076075925428822", "1000", "1000")