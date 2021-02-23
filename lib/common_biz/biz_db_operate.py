#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/22 10:20
# comment:
from lib.common.file_operation.config_operation import Config
from lib.common.logger.logging import Logger
from lib.common_biz.find_database_table import SeparateDbTable
from lib.common.utils.globals import GlobarVar
from lib.config.path import common_sql_path

mysql = GlobarVar.MYSQL_IN
logger = Logger('fiz_db_operate').get_logger()


def get_balance(ssoid):
    """
    查询可币余额
    :param ssoid:
    :return:
    """
    db_balance_info = SeparateDbTable(ssoid).get_coin_db_table()
    balance = mysql.select_one(
        str(Config(common_sql_path).read_config("nearme", "sql_balance")).format(db_balance_info[0], db_balance_info[1],
                                                                                 ssoid))['balance']
    logger.info("可币余额：{}".format(balance))
    return balance


def get_pay_req_by_partner(ssoid, partnerOrder):
    """
    根据商户订单号查询支付订单号
    :return:
    """
    db_order_info = SeparateDbTable(ssoid).get_order_db_table()
    pay_req_id = mysql.select_one(str(Config(common_sql_path).read_config("order", "partner_to_pay")).
                                          format(db_order_info[0], db_order_info[1], ssoid, partnerOrder))
    logger.info("查询到partnerOrder：{}， 对应支付订单号：{}".format(partnerOrder, pay_req_id))
    return pay_req_id['pay_req_id']


def get_contract_code(pay_req_id):
    """
    根据pay_req_id查询签约订单号
    :param pay_req_id:
    :return:
    """
    contract_code = mysql.select_one(str(Config(common_sql_path).read_config("order", "pay_to_contract")).
                                          format(pay_req_id))['contract_code']
    return contract_code


def update_sign_status(ssoid, pay_type, partner_code="2031", renew_product_code="20310001"):
    """
    更新autorenew_sign_info表，sign->unsign
    :return:
    """
    mysql.execute(str(Config(common_sql_path).read_config("order", "sign_to_un")).format(ssoid, partner_code, renew_product_code, pay_type))


if __name__ == '__main__':
    update_sign_status("", "wxpay")
