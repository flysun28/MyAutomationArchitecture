#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/9 15:24
# comment:
from lib.common.file_operation.config_operation import Config
from lib.common.utils.globals import GlobarVar
from lib.common.utils.meta import WithLogger
from lib.config.path import common_sql_path


class FindMerchant(metaclass=WithLogger):
    def __init__(self, partner_code):
        """
        :param partner_code: 业务线
        """
        self.partner_id = partner_code
        self.mysql = GlobarVar.MYSQL_IN

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


if __name__ == '__main__':
    A = FindMerchant("2031").find_app_id_merchant("wxpay")
    a = FindMerchant("2031").find_app_id_merchant_sign("wxpay")