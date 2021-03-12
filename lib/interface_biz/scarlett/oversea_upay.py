#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/24 20:13
# comment:
import requests
from lib.common.logger.logging import Logger
from lib.common.utils.env import get_env_config
from lib.common_biz.order_random import RandomOrder

logger = Logger('upay-scarlet').get_logger()


def upay_pay_scarlet(amount, cpOrderId):
    """
        "amount": "1000000", 分
        "appKey": "10000096",
        "area": "",
        "chKey": "default",
        "cpOrderId": "VN202102241123392076075925201703",
        "extra": "",
        "goodsKey": "GSK182",
        "hash": "85238588E261A537E855FF9740A5BDE7",
        "op": "92",
        "result": "200",
        "test": "true",
        "tradeId": "210224182311113568", 回调id
        "ts": "1614165820000",
        "uid": "ZING"
    """
    scarlet_data = {
        # 渠道回调为分，接口传入为元
        "amount": amount*100,
        "cpOrderId": cpOrderId,
        "hash": "85238588E261A537E855FF9740A5BDE7",
        "tradeId": RandomOrder(18).random_num(),
        "ts": RandomOrder(13).random_num(),
        "uid": "ZING"
    }
    scarlet_string = "amount={}&" \
                     "appKey=10000096&" \
                     "area=&" \
                     "chKey=default&" \
                     "cpOrderId={}&" \
                     "extra=&" \
                     "goodsKey=GSK182&" \
                     "hash=85238588E261A537E855FF9740A5BDE7&" \
                     "op=92&" \
                     "result=200&" \
                     "test=true&" \
                     "tradeId={}&" \
                     "ts={}&" \
                     "uid=ZING".format(str(scarlet_data['amount']), scarlet_data['cpOrderId'],
                                       scarlet_data['tradeId'], scarlet_data['ts'])
    response = requests.get(get_env_config()['url']['pay_scarlet_out'] + "/opaycenter/upaynotify?" + scarlet_string)
    result = response.content
    logger.info(str(result.decode("utf-8")))


if __name__ == '__main__':
    upay_pay_scarlet(10000, "VN202102241123392076075925201703")
