#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/9 11:39
# comment:
import time
import requests
from lib.common.algorithm.md5 import md5
from lib.common.file_operation.config_operation import Config
from lib.common.logger.logging import Logger
from lib.common.utils.env import get_env_config
from lib.common_biz.file_path import key_path
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign

logger = Logger('alipay-scarlet').get_logger()


def ali_normal_pay_scarlet(seller_email, out_trade_no, price, total_fee, seller_id, trade_status="TRADE_SUCCESS"):
    """
        "seller_email": "kekezhifu@keke.cn"
        "notify_id": "2021011400222173411016601413333125"
        "out_trade_no": "KB202101141734052076075925672072"
        "price": "0.01" 元
        "trade_status": "TRADE_SUCCESS" , "WAIT_BUYER_PAY"
        "total_fee": "0.01" 元
        "trade_no": "2021011422001416601409446457" 支付宝侧订单号
        "seller_id": "2088311951685799" 商户号
    :param seller_email:
    :param out_trade_no:
    :param price:
    :param total_fee:
    :param seller_id:
    :param trade_status:
    :return:
    """
    scarlett_info = {
        "gmt_create": time.strftime('%Y%m%d%H%M%S', time.localtime()),
        "buyer_email": "157****2782",
        "notify_time": time.strftime('%Y%m%d%H%M%S', time.localtime()),
        "seller_email": seller_email,
        "quantity": "1",
        "subject": "充值可币",
        "use_coupon": "N",
        "sign": "",
        "discount": "0.00",
        "body": "充值可币",
        "buyer_id": "2088612982416601",
        "notify_id": RandomOrder(32).random_num(),
        "notify_type": "trade_status_sync",
        "payment_type": "1",
        "out_trade_no": out_trade_no,
        "price": price,
        "trade_status": trade_status,
        "total_fee": total_fee,
        "trade_no": RandomOrder(28).random_num(),
        "sign_type": "RSA",
        "seller_id": seller_id,
        "is_total_fee_adjust": "Y"
    }
    logger.info("回调参数：{}".format(scarlett_info))
    # key自行生成，存放在配置文件中
    scarlett_info['sign'] = md5(Sign(scarlett_info).join_asc_have_key("", "sign_type") +
                                Config(key_path).read_config("key_private_ali", "value"))
    response = requests.post(get_env_config()['url']['pay_scarlet'] + "/opaycenter/notifypluginreader", data=scarlett_info)
    result = response.content
    logger.info(str(result.decode("utf-8")))


def ali_sign_scarlet():
    scarlett_info = {
        'gmt_create': time.strftime('%Y%m%d%H%M%S', time.localtime()),
        'charset': 'UTF-8',
        'gmt_payment': time.strftime('%Y%m%d%H%M%S', time.localtime()),
        'notify_time': time.strftime('%Y%m%d%H%M%S', time.localtime()),
        'subject': '签约并支付测试',
        'sign': '',
        'buyer_id': '2088112811111403',
        'body': '签约并支付测试',
        'invoice_amount': '0.01',
        'version': '1.0',
        'notify_id': RandomOrder(32).random_num(),
        'fund_bill_list': '[{"amount":"0.01","fundChannel":"PCREDIT"}]',
        'notify_type': 'trade_status_sync',
        'out_trade_no': 'RM202101141946232076075925873742',
        'total_amount': '0.01',
        'trade_status': 'TRADE_SUCCESS',
        'trade_no': '2021011422001411401404979184',
        'auth_app_id': '2016120904060189',
        'receipt_amount': '0.01',
        'point_amount': '0.00',
        'buyer_pay_amount': '0.01',
        'app_id': '2016120904060189',
        'sign_type': 'RSA2',
        'seller_id': '2088021161753879'
    }
    scarlett_info['sign'] = md5(Sign(scarlett_info).join_asc_have_key("", "sign_type") +
                                Config(key_path).read_config("key_private_ali", "value"))
    logger.info("回调参数：{}".format(scarlett_info))
    response = requests.post(get_env_config()['url']['pay_scarlet'] + "/opaycenter/alipayavoidpaynotifynew",
                             data=scarlett_info)
    result = response.content
    logger.info(str(result.decode("utf-8")))
    result = response.content
    logger.info(str(result.decode("utf-8")))
    if "SUCCESS" in str(result.decode("utf-8")):
        logger.info("回调解析成功")


if __name__ == '__main__':
    ali_sign_scarlet()
    #ali_normal_pay_scarlet("kekezhifu@keke.cn", "RM202102091449342076075925647732", "0.01", "0.01", "2088311951685799")