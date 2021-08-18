#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/9 15:09
# comment:
import datetime
import time
import requests
from lib.common.logger.logging import Logger
from lib.common.utils.env import get_env_config, set_global_env_id
from lib.common.utils.globals import HTTPJSON_SCARLET
from lib.common_biz.biz_db_operate import get_notify_id_by_request_id
from lib.common_biz.order_random import RandomOrder
from lib.interface_biz.scarlett.json_to_xml import wx_normal_pay_to_xml, wx_sign_to_xml, wx_mock_refund_to_xml
from lib.common_biz.find_merchant_info import FindMerchant
from lib.common_biz.find_key import GetKey

logger = Logger('wxpay-scarlet').get_logger()


def wx_normal_pay_scarlet(mch_id, out_trade_no, appid, total_fee, md5_key, trade_type="APP", attach="TEST", result_code="SUCCESS", return_code="SUCCESS"):
    """
    微信普通app支付回调报文构造 /opaycenter/WxpayNotificationSecondary
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
    微信签约回调报文 /opaycenter/wxpaysignnotify
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


def wx_sign_scarlet_by_raw_xml(raw_xml:str):
    '''
    从支付宝回调的原始结果（等号连接格式），重新构造签约回调
    :param raw_xml: '{gmt_create=2021-04-26 14:34:00, charset=UTF-8, ...}'
    '''    
    
    result = HTTPJSON_SCARLET.post('/opaycenter/alipayavoidnotifynew', data=raw_xml, lib=requests)
    if "SUCCESS" in str(result):
        logger.info("回调解析成功")


def wx_refund_post():
    """
    非异步，同步回调 https://api.mch.weixin.qq.com/secapi/pay/refund
    <xml>
    <appid>wx93eea96ecc33f168</appid>
    <mch_id>1259634601</mch_id>
    <nonce_str>ec287d47a74e4e21abf94300eec5cfa3</nonce_str>
    <transaction_id>4200000987202103020372370078</transaction_id>
    <sign>9450888586024CF0C4A700D03DFBDC79</sign>
    <out_trade_no>RM202103022135402076075925364572</out_trade_no>
    <out_refund_no>20210302213557592536457225602334</out_refund_no>
    <total_fee>1</total_fee>
    <refund_fee>1</refund_fee>
    <refund_fee_type>CNY</refund_fee_type>
    <op_user_id>1259634601</op_user_id>
    </xml>
    :return:
    """
    wx_refund_info = {
        "appid": "wx93eea96ecc33f168",
        "mch_id": "1259634601",
        "nonce_str": "ec287d47a74e4e21abf94300eec5cfa3",
        "transaction_id": "4200000987202103020372370078",
        "sign": "",
        "out_trade_no": "RM202103022135402076075925364572",
        "out_refund_no": "20210302213557592536457225602334",
        "total_fee": "1",
        "refund_fee": "1",
        "refund_fee_type": "CNY",
        "op_user_id": "1259634601"
    }


def wx_refund_mock_scarlett(pay_req_id, refund_fee, total_fee, cash_fee, cash_refund_fee):
    """
    :param pay_req_id:
    :param refund_fee: 分
    :param total_fee: 分
    :param cash_fee: 分
    :param cash_refund_fee: 分
    :return:
    """
    """
    <xml><return_code><![CDATA[SUCCESS]]></return_code>
    <return_msg><![CDATA[OK]]></return_msg>
    <appid><![CDATA[wx93eea96ecc33f168]]></appid>
    <mch_id><![CDATA[1259634601]]></mch_id>
    <nonce_str><![CDATA[D4u7oaArJWL62aY2]]></nonce_str>
    <sign><![CDATA[EB67A6ADF5ECDA485243DAEE3E3AE9EE]]></sign>
    <result_code><![CDATA[SUCCESS]]></result_code>
    <transaction_id><![CDATA[4200000987202103020372370078]]></transaction_id>
    <out_trade_no><![CDATA[RM202103022135402076075925364572]]></out_trade_no>
    <out_refund_no><![CDATA[20210302213557592536457225602334]]></out_refund_no>
    <refund_id><![CDATA[50301007512021030206765005243]]></refund_id>
    <refund_channel><![CDATA[]]></refund_channel>
    <refund_fee>1</refund_fee>
    <coupon_refund_fee>0</coupon_refund_fee>
    <total_fee>1</total_fee>
    <cash_fee>1</cash_fee>
    <coupon_refund_count>0</coupon_refund_count>
    <cash_refund_fee>1</cash_refund_fee></xml>
    :return:
    """
    wx_refund_info = {
        "return_code": "SUCCESS",
        "return_msg": "OK",
        "appid": "wx93eea96ecc33f168",
        "mch_id": "1259634601",
        "nonce_str": "D4u7oaArJWL62aY2",
        "sign": "",
        "result_code": "SUCCESS",
        "transaction_id": get_notify_id_by_request_id(pay_req_id),
        "out_trade_no": pay_req_id,
        "out_refund_no": RandomOrder(32).random_num(),
        "refund_id": RandomOrder(29).random_num(),
        "refund_channel": "",
        "refund_fee": refund_fee,
        "coupon_refund_fee": "0",
        "total_fee": total_fee,
        "cash_fee": cash_fee,
        "coupon_refund_count": "0",
        "cash_refund_fee": cash_refund_fee
    }
    logger.info("mock报文：{}".format(wx_refund_info))
    if get_notify_id_by_request_id(pay_req_id) == "False":
        return "pay_req_id is error"
    else:
        return wx_mock_refund_to_xml(wx_refund_info, "3007b2945cab4fd994341dc6edb65f33")


def wx_un_sign(params):
    result = HTTPJSON_SCARLET.post('/opaycenter/wxpaysignnotify', data=params)
    if "SUCCESS" in str(result):
        logger.info("回调解析成功")



class WxPayScarlett():
    
    def __init__(self, partner_code):
        FindMerchant(partner_code)
        self.merchant_info = FindMerchant(partner_code).find_app_id_merchant("wxpay")        
        self.md5_key = GetKey("").get_md5_key_from_merchant(self.merchant_info["app_id"], self.merchant_info["merchant_no"], "wxpay")
    
    def normal_pay_scarlett(self, out_trade_no, total_fee, trade_type="APP", attach="TEST", result_code="SUCCESS", return_code="SUCCESS"):
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
            "mch_id": self.merchant_info['merchant_no'],
            "cash_fee": "1",
            "out_trade_no": out_trade_no,
            "appid": self.merchant_info['app_id'],
            "total_fee": total_fee,
            "trade_type": trade_type,
            "result_code": result_code,
            "attach": attach,
            "time_end": time.strftime('%Y%m%d%H%M%S', time.localtime()),
            "is_subscribe": "N",
            "return_code": return_code
        }
        wx_scarlet_dict = wx_normal_pay_to_xml(wx_scarlet, self.md5_key)
        logger.info("回调参数：{}".format(wx_scarlet_dict))
        response = requests.post(get_env_config()['url']['pay_scarlet'] + "/opaycenter/WxpayNotificationSecondary",
                                 data=wx_scarlet_dict.encode("utf-8"))
        result = response.content
        logger.info(str(result.decode("utf-8")))
        if "SUCCESS" in str(result.decode("utf-8")):
            logger.info("回调解析成功")
        

if __name__ == '__main__':
    # set_global_env_id(1)
    #wx_refund_mock_scarlett("", "1", "1", "1", "1")
#     wx_normal_pay_scarlet("1259634601", "RM20210303222400207607592553078t", "wx93eea96ecc33f168", "1", "g4rTCeoBJFG4KyWCjTQCqltfEDma3yxR")
#     wx_scarlett = WxPayScarlett('5456925')
#     wx_scarlett.normal_pay_scarlett("KB202103111519232086100900845042", "3")
    wx_xml = "{charset=UTF-8, notify_time=2021-08-07 15:08:11, alipay_user_id=2088112811111403, sign=eNIekOabUlLoislnJHxn3mmUv/VGyxhWZRDv9HXl+3vhCx3njahn0aOUOdY8ZBKu7IW+nkubznC98sqj2Zg8N42WuMLHiq/rO3kim6erCRKmGXNc6CmjsOMD1zPfZMHa7AWMdXp7nizbbCPpKIEMLbHxn4unWsmvmxgmlkywpGvDE0Yi7QMuuygT8fARHvw9AJCObe8DY3SSaVVOQBsoRJUyAqB9HRTcYLdGS1/L7lEzSJCbhVxIrMgQ14xApCCgmaJNBHR6yGIQWs0FXWgBnekbNgjH33GKA2RipMdCHakAotSI/FD+dfWM1oFLqnklcfgQkvCZNmN8xoNR87xG3A==, external_agreement_no=SN202108071507493132734376823351, version=1.0, sign_time=2021-08-07 15:08:11, notify_id=2021080700222150811023361457182243, notify_type=dut_user_sign, agreement_no=20215607750930630440, auth_app_id=2021001186651417, invalid_time=2115-02-01 00:00:00, personal_product_code=GENERAL_WITHHOLDING_P, valid_time=2021-08-07 15:08:11, app_id=2021001186651417, sign_type=RSA2, alipay_logon_id=156******06, status=NORMAL, sign_scene=INDUSTRY|GAME_CHARGE}"
    wx_un_sign(wx_xml)
