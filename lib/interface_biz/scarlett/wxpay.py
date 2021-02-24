#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/9 15:09
# comment:
import datetime
import time
import requests
from lib.common.logger.logging import Logger
from lib.common.utils.env import get_env_config
from lib.common_biz.order_random import RandomOrder
from lib.interface_biz.scarlett.json_to_xml import wx_normal_pay_to_xml, wx_sign_to_xml

logger = Logger('wxpay-scarlet').get_logger()


def wx_normal_pay_scarlet(mch_id, out_trade_no, appid, total_fee, md5_key, trade_type="APP", attach="TEST", result_code="SUCCESS", return_code="SUCCESS"):
    """
    微信普通app支付回调报文构造
    :param mch_id: 商户号 1259634601
    :param out_trade_no: 支付订单号 RM202101131635122076075925041132
    :param appid: appid wx93eea96ecc33f168
    :param total_fee: 金额 2 分
    :param trade_type: 支付方式 APP
    :param attach: 附加数据 RM202101131635122076075925041132
    :param result_code: SUCCESS
    :param return_code: SUCCESS
    transaction_id： 微信支付系统生成的订单号
    :return:
    """
    wx_scarlet = {
        "transaction_id": RandomOrder(28).random_num(),
        "nonce_str": RandomOrder(32).random_string(),
        "bank_type": "OTHERS",
        "openid": "oCg6Xt8NvRi7jGuap_5B6XdY4oYk",
        "sign": "",
        "fee_type": "CNY",
        "mch_id": mch_id,
        "cash_fee": "1",
        "out_trade_no": out_trade_no,
        "appid": appid,
        "total_fee": total_fee,
        "trade_type": trade_type,
        "result_code": result_code,
        "attach": attach,
        "time_end": time.strftime('%Y%m%d%H%M%S', time.localtime()),
        "is_subscribe": "N",
        "return_code": return_code
    }
    wx_scarlet_dict = wx_normal_pay_to_xml(wx_scarlet, md5_key)
    logger.info("回调参数：{}".format(wx_scarlet_dict))
    response = requests.post(get_env_config()['url']['pay_scarlet'] + "/opaycenter/WxpayNotificationSecondary",
                             data=wx_scarlet_dict.encode("utf-8"))
    result = response.content
    logger.info(str(result.decode("utf-8")))
    if "SUCCESS" in str(result.decode("utf-8")):
        logger.info("回调解析成功")


def wx_sign_scarlet(contract_code, mch_id, plan_id, md5_key, result_cod="SUCCESS", return_code="SUCCESS", return_msg="OK", change_type="ADD"):
    """
    微信签约回调报文
    :param change_type: ?
    :param result_cod:
    :param contract_code: 签约订单号 SN202101132002474706373405162488
    :param contract_id:  对应数据库merchant_no，签约协议号--微信侧 202101135861021321
    :param mch_id: 对应数据库merchant_no，商户号 1259634601
    :param plan_id: 数据库对应plan_id 131584
    :param request_serial: 微信订单号？ 161053936774063070
    :param result_code: SUCCESS
    :param return_code: SUCCESS
    :param return_msg: OK
    :return:
    """
    now = datetime.datetime.now()
    end_time = now + datetime.timedelta(days=365)
    end_time = str(end_time.strftime('%Y-%m-%d %H:%M:%S'))
    wx_scarlet = {
        "change_type": change_type,
        "contract_code": contract_code,
        # 未来时间 续费时间？
        "contract_expired_time": end_time,
        "contract_id": RandomOrder(10).random_num(),
        "mch_id": mch_id,
        # 微信用户表示
        "openid": "oCg6Xt8NvRi7jGuap_5B6XdY4oYk",
        "operate_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "plan_id": plan_id,
        "request_serial": RandomOrder(18).random_num(),
        "result_code": result_cod,
        "return_code": return_code,
        "return_msg": return_msg,
        "sign": ""
    }
    wx_scarlet_dict = wx_sign_to_xml(wx_scarlet, md5_key)
    logger.info("回调参数：{}".format(wx_scarlet_dict))
    response = requests.post(get_env_config()['url']['pay_scarlet'] + "/opaycenter/wxpaysignnotify",
                             data=wx_scarlet_dict.encode("utf-8"))
    result = response.content
    logger.info(str(result.decode("utf-8")))
    if "SUCCESS" in str(result.decode("utf-8")):
        logger.info("回调解析成功")


if __name__ == '__main__':
    pass
