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
from lib.common_biz.biz_db_operate import get_notify_id_by_request_id
from lib.common_biz.file_path import key_path
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign
from lib.interface_biz.scarlett.map_to_json import scarlet_map_to_json,\
    scarlet_map_to_json_
from lib.common.utils.globals import HTTPJSON_IN, HTTPJSON_SCARLET

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
    :param out_trade_no: 支付订单号
    :param price:
    :param total_fee:
    :param seller_id: 支付商户号（支付充当卖家）
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
    """
    未使用，秘钥未更改
    :return:
    """
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
#         'seller_id': '2088021161753879',
        'seller_id': '2088311951685799'
    }
    scarlett_info['sign'] = md5(Sign(scarlett_info).join_asc_have_key("", "sign_type") +
                                Config(key_path).read_config("key_private_ali", "value"))
    logger.info("回调参数：{}".format(scarlett_info))
    response = requests.post(get_env_config()['url']['pay_scarlet'] + "/opaycenter/alipayavoidnotifynew",
                             data=scarlett_info)
    result = response.content
    logger.info(str(result.decode("utf-8")))
    if "SUCCESS" in str(result.decode("utf-8")):
        logger.info("回调解析成功")
        

def ali_sign_scarlet_by_raw_resp(raw_map:str):
    '''
    将支付宝回调的原始签约报文（等号连接格式），转换成字典格式。重新发给Scarlett
    :param raw_map: '{gmt_create=2021-04-26 14:34:00, charset=UTF-8, ...}'
    '''    
    scarlett_info = scarlet_map_to_json_(raw_map)
    result = HTTPJSON_SCARLET.post('/opaycenter/alipayavoidnotifynew', data=scarlett_info, lib=requests)
    if "SUCCESS" in str(result):
        logger.info("回调解析成功")


def ali_pay_refund(amount, pay_req_id):
    """
    amount: 元
    notify_id: 订单表支付notify_id
    支付宝渠道退款
    去除sign、sign_type字段，排序后拼接=&，最后一个&去掉 拼接key做md5得到sign
    key: `platform_opay`.`channel_merchant_info` 根据商户号查询
    {notify_type=batch_refund_notify, notify_time=2021-02-25 17:22:02, batch_no=20210225172200090072222223155616,
    success_num=1, sign=bcbc3fb4adcfc3b71029cce20a4d77cc, sign_type=MD5,
    result_details=2021022522001448571439840247^0.01^SUCCESS, notify_id=2021022500222172202075461444782769}
    :return:
    """
    scarlett_info = {"notify_type": "batch_refund_notify",
                     "notify_time": time.strftime('%Y-%m-%d- %H:%M:%S', time.localtime()),
                     "batch_no": RandomOrder(32).random_num(),
                     "success_num": amount*100,
                     "sign": "",
                     "sign_type": "MD5",
                     "result_details": "{}^{}^SUCCESS".format(get_notify_id_by_request_id(pay_req_id), amount),
                     "notify_id": RandomOrder(32).random_num()}
    scarlett_info['sign'] = md5(Sign(scarlett_info).join_asc_have_key("", "sign_type") + "vle91cs2yv9g9w61f0dd8ev5sug0smo5")
    logger.info("传入的回调报文：{}".format(scarlett_info))
    response = requests.post(get_env_config()['url']['pay_scarlet'] + "/opaycenter/alipayrefundnotify",
                             data=scarlett_info)
    result = response.content
    logger.info(str(result.decode("utf-8")))


if __name__ == '__main__':
    ali_sign_scarlet()
    #ali_normal_pay_scarlet("kekezhifu@keke.cn", "RM202102091449342076075925647732", "0.01", "0.01", "2088311951685799")
#     ali_pay_refund(0.01, "RM202103031056412076075925884122")
