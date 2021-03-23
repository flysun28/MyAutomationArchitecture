#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/9 15:24
# comment:
from lib.common.file_operation.config_operation import Config
from lib.common.utils.env import get_env_id
from lib.common.utils.globals import GlobalVar, MYSQL_AUTO_TEST
from lib.common.utils.meta import WithLogger
from lib.config.path import common_sql_path


class FindMerchant(metaclass=WithLogger):
    '''
    业务线私钥
    '''
    def __init__(self, partner_code):
        """
        :param partner_code: 业务线
        """
        self.partner_id = partner_code
        self.mysql = GlobalVar.MYSQL_IN

    def find_app_id_merchant(self, channel):
        """
        `platform_opay`.`partner_map_merchant`
        :return:
        """
        try:
            sql_merchant = str(Config(common_sql_path).read_config("platform_opay", "find_merchant")).format(self.partner_id, channel)
            merchant = self.mysql.select(sql_merchant)[0]
            self.logger.info("查询到商户信息：{}".format(merchant))
            return merchant
        except Exception as e:
            self.logger.info(e)

    def find_app_id_merchant_sign(self, channel):
        """
        `platform_opay`.`partner_map_merchant`
        :return:
        """
        try:
            sql_merchant = str(Config(common_sql_path).read_config("platform_opay", "find_merchant_sign")).format(self.partner_id, channel)
            merchant = self.mysql.select(sql_merchant)[0]
            self.logger.info("查询到商户信息：{}".format(merchant))
            return merchant
        except Exception as e:
            self.logger.info(e)


def find_merchant_info(channel, partner_id):
    """
    渠道私钥
    :param partner_id: 2031
    :param channel: wxpay,qq_pay,szf_pay,heepay
    :return:
    """
    env_id = get_env_id()
    mysql = MYSQL_AUTO_TEST
    flag = ""
    if env_id == "1" or env_id == "2" or env_id == "3":
        flag = "test"
    if env_id == "grey" or env_id == "product":
        flag = "product"
    '''
    test_merchant = SELECT * FROM `pay_auto_test_info`.`test_env_merchant_info` WHERE partner_id = "{}" AND channel = "{}"
    product_merchant = SELECT * FROM `pay_auto_test_info`.`product_env_merchant_info` WHERE partner_id = "{}" AND channel = "{}"
    '''
    pay_merchant = mysql.select_one(
        (Config(common_sql_path).read_config('pay_auto_test_info', '{}_merchant'.format(flag))).format(partner_id, channel)
    )
    return pay_merchant


if __name__ == '__main__':
    A = FindMerchant("2031").find_app_id_merchant("wxpay")
    a = FindMerchant("2031").find_app_id_merchant_sign("wxpay")