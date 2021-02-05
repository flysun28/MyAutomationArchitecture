#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 22:53
# comment: 查询秘钥相关
from common.db_operation.mysql_operation import connect_mysql
from common.file_operation.config_operation import Config
from common.utils.meta import WithLogger
from config.path import common_sql_path
from pymysql.err import DataError
from common.utils.globals import GlobarVar


class GetKey(metaclass=WithLogger):
    __SECRET_KEYS = {}
    
    def __init__(self, partner_id, in_out='inland'):
        """
        :param partner_id: 业务线
        """
        self.partner_id = partner_id
        if getattr(self, 'mysql', None) is None:
            self.mysql = GlobarVar.MYSQL_IN if in_out == 'inland' else GlobarVar.MYSQL_OS
#         self.mysql = connect_mysql(in_out)

    def get_key_from_merchant(self):
        """
        查找`db_order_0`.`merchant_info`业务线对应秘钥
        :return:
        """
        existed = self.__SECRET_KEYS.get(self.partner_id)
        if existed:
            return existed
        try:
            sql_key = str(Config(common_sql_path).read_config("merchant", "sql_key")).format(self.partner_id)
            res = self.mysql.select_one(sql_key)
            assert res
            key = res['merchant_key']
            self.logger.info("查询到秘钥信息：{}".format(key))
            self.__SECRET_KEYS.setdefault(self.partner_id, key)
            return key
        except AssertionError:
            raise DataError('在merchant_info中无法匹配出"%s"的私钥' %self.partner_id) from None
        except:
            import sys
            self.logger.info(sys._getframe()[1])

    def get_key_from_partner_key(self):
        """
        查找`platform_opay`.`partner_key`
        :return:
        """
        try:
            sql_key = str(Config(common_sql_path).read_config('db_platform_gateway', 'sql_partner_key')).format(self.partner_id)
            KEY = self.mysql.select_one(sql_key)["partner_public_key"]
            self.logger.info("查询到秘钥信息：{}".format(KEY))
            return KEY
        except Exception as e:
            self.logger.info(e)

    def get_key_from_t_key(self):
        """
        查找`platform_opay`.`t_key`秘钥
        :return:
        """
        try:
            sql_key = str(Config(common_sql_path).read_config('db_platform_gateway', 'sql_t_key')).format(self.partner_id)
            KEY = self.mysql.select_one(sql_key)["md5_key"]
            self.logger.info("查询到秘钥信息：{}".format(KEY))
            return KEY
        except Exception as e:
            self.logger.info(e)

    def get_key_from_voucher(self):
        """
        `oppopay_voucher`.`vou_appinfo`
        :return:
        """
        try:
            sql_key = str(Config(common_sql_path).read_config('voucher', 'voucher_key')).format(self.partner_id)
            KEY = self.mysql.select_one(sql_key)["appkey"]
            self.logger.info("查询到秘钥信息：{}".format(KEY))
            return KEY
        except Exception as e:
            self.logger.info(e)

    def get_key_from_server_info(self):
        """
        gateway配置dubbo路由key
        `db_platform_gateway`.`server_app_info`
        :return:
        """
        try:
            sql_key = str(Config(common_sql_path).read_config('key', 'sql_key')).format(self.partner_id)
            KEY = self.mysql.select_one(sql_key)["app_key"]
            self.logger.info("查询到秘钥信息：{}".format(KEY))
            return KEY
        except Exception as e:
            self.logger.info(e)

    def get_md5_key_from_merchant(self, app_id, merchant_no, pay_channel):
        """
        查找`platform_opay`.`channel_merchant_info`
        :return:
        """
        try:
            sql_key = str(Config(common_sql_path).read_config('platform_opay', 'sql_md5_key')).format(app_id, merchant_no, pay_channel)
            KEY = self.mysql.select_one(sql_key)["md5_key"]
            self.logger.info("查询到秘钥信息：{}".format(KEY))
            return KEY
        except Exception as e:
            self.logger.info(e)



if __name__ == '__main__':
    # A = GetKey("2031").get_key_from_partner_key()
    GetKey("5456925").get_key_from_voucher()