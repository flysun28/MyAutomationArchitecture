#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/9 15:04
# comment:
import _thread

import requests
from lib.common.algorithm.md5 import md5
from lib.common.logger.logging import Logger
from lib.common.utils.env import get_env_config
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import hee_pay_sign_string
logger = Logger('heepay-scarlet').get_logger()


def hee_pay_notify(bill_id, card_real_amt):
    """
    "bill_id": "KB202101141240530447214926427550" 支付订单号
    "card_real_amt": "100.00" 回调金额 元
    "jnet_bill_no": 回调id
    :return:
    """
    jnet_bill_no = RandomOrder(28).random_num()
    scarlet_data = {
        "bill_id": bill_id,
        "agent_id": "1715258",
        "sign": "",
        "ret_msg": "-%b2%e9%d1%af%b4%a6%c0%ed",
        "card_settle_amt": "0.00",
        "ret_code": "0",
        "bill_status": "1",
        "card_real_amt": str(card_real_amt),
        "jnet_bill_no": jnet_bill_no
    }
    sign_string = hee_pay_sign_string(scarlet_data)
    scarlet_data['sign'] = md5(sign_string, to_upper=False)
    notify_string = 'ret_msg=-%b2%e9%d1%af%b4%a6%c0%ed&' \
                    'ret_code=0&' \
                    'bill_status=1&' \
                    'agent_id=1715258&' \
                    'bill_id={}&' \
                    'jnet_bill_no={}&' \
                    'card_settle_amt=0.00&' \
                    'card_real_amt={}&' \
                    'card_detail_data=&' \
                    'ext_param=&' \
                    'sign={}'.format(scarlet_data['bill_id'],  scarlet_data['jnet_bill_no'], scarlet_data['card_real_amt'], scarlet_data['sign'])
    url = get_env_config()['url']['pay_scarlet'] + "/opaycenter/heepaynotify?" + notify_string
    logger.info("回调参数：{}".format(url))
    response = requests.get(url)
    result = response.content
    logger.info("返回结果：".format(result))


if __name__ == '__main__':
    hee_pay_notify('KB202102191602452076075925013522', '5')
    hee_pay_notify('KB202102191602452076075925013522', '5')
    # hee_pay_notify('KB202102191424402076075925814832', '20')