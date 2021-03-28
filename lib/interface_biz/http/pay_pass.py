#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 22:56
# comment: 鉴权接口
from lib.common.algorithm.other import get_RV
from lib.common.file_operation.config_operation import Config
from lib.common.logger.logging import Logger
from lib.common.session.http.protobuf import ProtoBuf
from lib.common.utils.env import get_env_config, set_global_env_id, get_env_id
from lib.common.utils.meta import WithLogger
from lib.config.path import common_sql_path
from lib.interface_biz.http.vip_login import Account
from lib.common_biz.order_random import RandomOrder
from lib.pb_src.python_native import PassPb_pb2
from lib.common.utils.globals import GlobalVar

logger = Logger('鉴权').get_logger()


def get_t_p(param):
    """
    :return:
    """
    url = get_env_config()["url"]["pay_in"] + "/tksv/post/pass"
    response = ProtoBuf(PassPb_pb2).runner(url, 'Request', param, flag=0)
    result = ProtoBuf(PassPb_pb2).parser('Result', response)
    if result.s_p and result.t_p:
        r_v = get_RV(result.s_p, step_count=4)
        return r_v, result.t_p, result.m_p


def get_check_t_p(param):
    """
    :return:
    """
    res = get_t_p(param)
    if res:
        return res
    else:
        token_new = Account().login()
        env_id = get_env_id()
        if env_id == "1":
            GlobalVar.MYSQL_AUTO_TEST.execute(
                Config(common_sql_path).read_config("pay_auto_test_info", "test_update_account").format(token_new))
        if env_id == "grey" or env_id == "product":
            GlobalVar.MYSQL_AUTO_TEST.execute(
                Config(common_sql_path).read_config("pay_auto_test_info", "product_update_account").format(token_new))
        logger.info('成功替换token:{} 并写入数据库'.format(token_new))
        # logger.info('成功将token:{} 并写入redis'.format(token_new))
        return get_t_p(param)


def pass_no_login_in():
    """
    国内返回传固定tp,rv
    :return:
    """
    t_p = "notokendefaulttp0123456789abcdef"
    r_v = "RvDf0ABC"
    m_p = ""
    return r_v, t_p, m_p


class Pass(metaclass=WithLogger):
    """
        返回t_p, r_v用作鉴权
        version: 直扣与无账号 version最新为6.0  充值/充值消费最新为11.0
        amount: 支付金额
        sdkVer: 支付版本，小的版本号
        url: 兼容海外账号不稳定，需要切换到国内进行鉴权
        partner: 业务线
        type: 直扣/无账号/不走收银台type=1, 充值/充值消费type=0
        token:
        package: 部分游戏有黑名单限制
        amount: 默认进入传入较大，为了适应优惠券的返回
    """

    def __init__(self, partner="2031", sdkVer="20602", amount="100000.0", package="com.example.pay_demo"):
        """
        """
        self.partner = partner
        self.sdkVer = sdkVer
        self.amount = amount
        self.package = package

    def pass_recharge(self, version="11.0", pay_type="0"):
        param = {
            "token": GlobalVar.TOKEN,
            "partner": self.partner,
            "package": self.package,
            "ext": "",
            "version": version,
            "appKey": "1234",
            "count": 10000,
            "order": RandomOrder(14).random_num(),
            "ip": "121.13.218.236",
            "type": pay_type,
            "sdkVer": self.sdkVer,
            "amount": self.amount,
            "gameSdkVer": 0,
            "partnerOrder": "",
            "notifyUrl": "http://pay.pay-test.wanyol.com/notify/notify/receiver",
            "country": "CN"
        }
        return get_check_t_p(param)

    def pass_recharge_spend(self, version="11.0", pay_type="0"):
        param = {
            "token": GlobalVar.TOKEN,
            "partner": self.partner,
            "package": self.package,
            "ext": "",
            "version": version,
            "appKey": "1234",
            "count": 10000,
            "order": RandomOrder(14).random_num(),
            "ip": "121.13.218.236",
            "type": pay_type,
            "sdkVer": self.sdkVer,
            "amount": self.amount,
            "gameSdkVer": 0,
            "partnerOrder": RandomOrder(32).random_string(),
            "notifyUrl": "http://pay.pay-test.wanyol.com/notify/notify/receiver",
            "country": "CN"
        }
        return get_check_t_p(param)

    def pass_direct_pay(self, version="6.0", pay_type="1"):
        """
        :param version:
        :param pay_type:
        :return:
        """
        param = {
            "token": GlobalVar.TOKEN,
            "partner": self.partner,
            "package": self.package,
            "ext": "",
            "version": version,
            "appKey": "1234",
            "count": 10000,
            "order": RandomOrder(14).random_num(),
            "ip": "121.13.218.236",
            "type": pay_type,
            "sdkVer": self.sdkVer,
            "amount": self.amount,
            "gameSdkVer": 0,
            "partnerOrder": RandomOrder(32).random_string(),
            "notifyUrl": "http://pay.pay-test.wanyol.com/notify/notify/receiver",
            "country": "CN"
        }
        return get_check_t_p(param)

    """
    def pass_demo(self, version="11.0", pay_type="0"):
        param = {
            "token": Config(account_path).read_config("account", "token"),
            "partner": self.partner,
            "package": self.package,
            "ext": "",
            "version": version,
            "appKey": "1234",
            "count": 10000,
            "order": RandomOrder(14).random_num(),
            "ip": "121.13.218.236",
            "type": pay_type,
            "sdkVer": self.sdkVer,
            "amount": self.amount,
            "gameSdkVer": 0,
            "partnerOrder": "",
            "notifyUrl": "http://pay.pay-test.wanyol.com/notify/notify/receiver",
            "country": "CN"
        }
        return get_check_t_p(param)
    """


if __name__ == '__main__':
    set_global_env_id(3)
    pass_ = Pass(partner="5456925", sdkVer="20600", amount="1.0", package="com.skymoons.hqg.nearme.gamecenter")
    print(pass_.pass_recharge_spend())
    # check_token()
    # b = Pass().pass_direct_pay()
