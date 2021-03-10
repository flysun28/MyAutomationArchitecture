#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/2 17:27
# comment:
import time
import requests
from lib.common.logger.logging import Logger
from lib.common.utils.env import get_env_config
from lib.common_biz.biz_db_operate import get_notify_id_by_request_id
from lib.common_biz.order_random import RandomOrder
from lib.interface_biz.scarlett.json_to_xml import qq_pay_to_xml, qq_mock_refund_to_xml

logger = Logger('qq-scarlet').get_logger()


def qq_pay_scarlet(pay_req_id, amount):
    """
    key = 46b3da6ee122993430adb1f7e20c4327
    <?xml version="1.0" encoding="UTF-8" ?><xml>
    <appid><![CDATA[1104946420]]></appid>
    <attach><![CDATA[KB202103020003060398398923646501]]></attach>
    <bank_type><![CDATA[BALANCE]]></bank_type>
    <cash_fee><![CDATA[100]]></cash_fee>
    <fee_type><![CDATA[CNY]]></fee_type>
    <mch_id><![CDATA[1282256301]]></mch_id>
    <nonce_str><![CDATA[33cc356eb0fa6bbb6189e1a94c5f53ef]]></nonce_str>
    <openid><![CDATA[6EC23B34AD89E14F95B5C39949348CBB]]></openid>
    <out_trade_no><![CDATA[KB202103020003060398398923646501]]></out_trade_no>
    <sign><![CDATA[14BD9312E41CB4A4156457B64B389F66]]></sign>
    <time_end><![CDATA[20210302000318]]></time_end>
    <total_fee><![CDATA[100]]></total_fee>
    <trade_state><![CDATA[SUCCESS]]></trade_state>
    <trade_type><![CDATA[APP]]></trade_type>
    <transaction_id><![CDATA[12822563016012202103021638971722]]></transaction_id></xml>
    :return:
    """
    qq_scarlet = {
        "appid": "1104946420",
        "attach": pay_req_id,
        "bank_type": "BALANCE",
        # 分
        "cash_fee": amount,
        "fee_type": "CNY",
        "mch_id": "1282256301",
        "nonce_str": RandomOrder(32).random_string(),
        "openid": "6EC23B34AD89E14F95B5C39949348CBB",
        "out_trade_no": pay_req_id,
        "sign": "",
        "time_end": time.strftime('%Y%m%d%H%M%S', time.localtime()),
        "total_fee": amount,
        "trade_state": "SUCCESS",
        "trade_type": "APP",
        "transaction_id": RandomOrder(32).random_num(),
    }
    req_scarlet = (qq_pay_to_xml(qq_scarlet, "46b3da6ee122993430adb1f7e20c4327"))
    response = requests.post(get_env_config()['url']['pay_scarlet'] + "/opaycenter/qqpayNotifycation",
                             data=req_scarlet.encode("utf-8"))
    result = response.content
    logger.info(str(result.decode("utf-8")))
    if "SUCCESS" in str(result.decode("utf-8")):
        logger.info("回调解析成功")


def qq_refund_post():
    """
    <xml><appid>1104946420</appid>
    <mch_id>1282256301</mch_id>
    <nonce_str>ba655fe9ca1643baadc4e556ca3a7188</nonce_str>
    <op_user_id>1282256301</op_user_id>
    <op_user_passwd>3c8d318f090f73e77da648a6654c7270</op_user_passwd>
    <out_refund_no>20210302213427592561556242617421</out_refund_no>
    <out_trade_no>RM202103022132002076075925615562</out_trade_no>
    <refund_fee>1</refund_fee>
    <sign>1C2D7315A7EB50F5ACE5A205FAC2B3A3</sign>
    <transaction_id>12822563016012202103021548430031</transaction_id>
    </xml>
    :return:
    """
    qq_refund_info = {"appid": "1104946420", "mch_id": "1282256301", "nonce_str": "ba655fe9ca1643baadc4e556ca3a7188",
                      "op_user_id": "1282256301", "op_user_passwd": "3c8d318f090f73e77da648a6654c7270",
                      "out_refund_no": "20210302213427592561556242617421",
                      "out_trade_no": "RM202103022132002076075925615562", "refund_fee": "1",
                      "transaction_id": "12822563016012202103021548430031", 'sign': ""}
    req_scarlet = ""
    req_scarlet = (qq_pay_to_xml(qq_refund_info, "46b3da6ee122993430adb1f7e20c4327"))
    response = requests.post(get_env_config()['url']['pay_scarlet'] + "/opaycenter/qqpayNotifycation",
                             data=req_scarlet.encode("utf-8"))
    result = response.content
    logger.info(str(result.decode("utf-8")))


def qq_refund_mock_scarlett(pay_req_id, refund_fee, total_fee):
    """
    :param pay_req_id:
    :param refund_fee: 分
    :param total_fee: 分
    :return:
    """
    """
    非异步返回，同步返回 https://api.qpay.qq.com/cgi-bin/pay/qpay_refund.cgi
    <?xml version="1.0" encoding="UTF-8" ?><xml>
    <return_code><![CDATA[SUCCESS]]></return_code>
    <return_msg><![CDATA[SUCCESS]]></return_msg>
    <retcode><![CDATA[0]]></retcode>
    <retmsg><![CDATA[ok]]></retmsg>
    <appid><![CDATA[1104946420]]></appid>
    <mch_id><![CDATA[1282256301]]></mch_id>
    <nonce_str><![CDATA[5d9062b72e65846f8b9b0a6e176ecce9]]></nonce_str>
    <openid><![CDATA[0D4E5B0D1AE1605ADD7EECFCA611DC84]]></openid>
    <out_refund_no><![CDATA[20210302213427592561556242617421]]></out_refund_no>
    <out_trade_no><![CDATA[RM202103022132002076075925615562]]></out_trade_no>
    <refund_channel><![CDATA[ORIGINAL]]></refund_channel>
    <refund_fee><![CDATA[1]]></refund_fee>
    <refund_id><![CDATA[12822563017012202103021639413456]]></refund_id>
    <result_code><![CDATA[SUCCESS]]></result_code>
    <sign><![CDATA[0383758DC46AABB0BE5D2333CDFBEB63]]></sign>
    <total_fee><![CDATA[1]]></total_fee>
    <transaction_id><![CDATA[12822563016012202103021548430031]]></transaction_id></xml>

    appid=1104946420&mch_id=1282256301&nonce_str=5d9062b72e65846f8b9b0a6e176ecce9&openid=0D4E5B0D1AE1605ADD7EECFCA611DC84&
    out_refund_no=20210302213427592561556242617421&out_trade_no=RM202103022132002076075925615562&refund_channel=ORIGINAL&
    refund_fee=1&refund_id=12822563017012202103021639413456&result_code=SUCCESS&retcode=0&retmsg=ok&return_code=SUCCESS&
    return_msg=SUCCESS&total_fee=1&transaction_id=12822563016012202103021548430031&key=
    :return:
    """
    qq_refund_info = {
        "return_code": "SUCCESS",
        "return_msg": "SUCCESS",
        "retcode": "0",
        "retmsg": "ok",
        "appid": "1104946420",
        "mch_id": "1282256301",
        "nonce_str": RandomOrder(32).random_string(),
        "openid": "0D4E5B0D1AE1605ADD7EECFCA611DC84",
        "out_refund_no": RandomOrder(32).random_num(),
        "out_trade_no": pay_req_id,
        "refund_channel": "ORIGINAL",
        "refund_fee": refund_fee,
        "refund_id": RandomOrder(32).random_num(),
        "result_code": "SUCCESS",
        "sign": "",
        "total_fee": total_fee,
        "transaction_id": get_notify_id_by_request_id(pay_req_id)
    }
    logger.info("mock报文：{}".format(qq_refund_info))
    if get_notify_id_by_request_id(pay_req_id) == "False":
        return "pay_req_id is error"
    else:
        return qq_mock_refund_to_xml(qq_refund_info, "46b3da6ee122993430adb1f7e20c4327")


if __name__ == '__main__':
    qq_pay_scarlet("KB202103091724082076075925432122", "1")
    #qq_refund_mock_scarlett("RM202103031056412076075925884122", "1", "1")
