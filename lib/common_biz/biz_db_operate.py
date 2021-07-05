#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/22 10:20
# comment:
import random
from itertools import product
from pymysql.err import MySQLError
from lib.common.file_operation.config_operation import Config
from lib.common.logger.logging import Logger
from lib.common_biz.find_database_table import SeparateDbTable
from lib.common.utils.globals import GlobalVar
from lib.config.path import common_sql_path
from lib.common.utils.constants import voucher_type_enum
from lib.common.utils.misc_utils import to_pinyin


mysql = GlobalVar.MYSQL_IN
mysql_out = GlobalVar.MYSQL_OUT
logger = Logger('fiz_db_operate').get_logger()


def get_ssoid_by_pay_req_id(pay_red_id):
    """
    根据支付订单号，查找ssoid
    :param pay_red_id:
    :return:
    """
    return pay_red_id[16: 26]


def get_balance(ssoid, country="CN", in_out="inland"):
    """
    查询可币余额
    :param country:
    :param in_out:
    :param ssoid:
    :return:
    """
    db_balance_info = SeparateDbTable(ssoid).get_coin_db_table()
    sql_balance = str(Config(common_sql_path).read_config("nearme", "sql_balance")).format(
                               db_balance_info[0], db_balance_info[1], ssoid, country)
    if in_out == "inland":
        balance = mysql.select_one(sql_balance)['balance']
        logger.info("可币余额：{}".format(balance))
        return balance
    elif in_out == "oversea":
        balance = mysql_out.select_one(sql_balance)['balance']
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


def oversea_get_coin_rate(currency):
    """
    海外查询汇率
    :param currency:
    :return:
    """
    rate = mysql_out.select_one(str(Config(common_sql_path).read_config("platform_opay", "coin_rate")).
                                          format(currency))['rate']
    return rate


def get_notify_id_by_request_id(pay_req_id):
    """
    根据支付订单号查询notify)id
    :return:
    """
    db_order_info = SeparateDbTable(get_ssoid_by_pay_req_id(pay_req_id)).get_order_db_table()
    notify_id = mysql.select_one(str(Config(common_sql_path).read_config("order", "notify_id")).
                                          format(db_order_info[0], db_order_info[1], pay_req_id))
    if notify_id is None:
        return "False"
    else:
        return notify_id['notify_id']


def _drop_spec_columns_on_all_order_tables(*args):
    '''
    仅内部使用
    '''
    sql = 'ALTER TABLE db_order_%d.order_info_%d\n'
    for arg in args:
        sql += f' DROP COLUMN `{arg}`,'
    lsql = sql.rsplit(',', 1)
    assert len(lsql) == 2
    lsql[-1] = ';'
    sql = ''.join(lsql)
    for db_order_id, order_info_id in product(range(8), range(128)): 
        sql_ = sql %(db_order_id, order_info_id)
        print(sql_)
        GlobalVar.MYSQL_IN.execute(sql_)


def _add_columns_on_all_order_tables(*args):
    '''
    仅内部使用
    '''
    if not args:
        return
    sql = 'ALTER TABLE db_order_%d.order_info_%d'
    for idx, arg in enumerate(args):
        appended = '\nADD COLUMN `%s` varchar(10) DEFAULT NULL'
        if idx == 0:
            appended += ','
            sql += appended %arg
        else:
            appended += ' AFTER `%s`,'
            sql += appended %(arg, args[idx-1])
    lsql = sql.rsplit(',', 1)
    assert len(lsql) == 2
    lsql[-1] = ';'
    sql = ''.join(lsql)
    for db_order_id, order_info_id in product(range(8), range(128)):
        sql_ = sql %(db_order_id, order_info_id)
        print(sql_)
        try:
            GlobalVar.MYSQL_IN.execute(sql_)
        except:
            raise


def get_available_voucher(ssoid, vou_key, partner_id='2031'):
    '''
    根据ssoid和类型查询可用的优惠券
    :param ssoid:
    :param vou_key: 代表查找优惠券的key值，可以为券id或券类型
                    券类型支持数字或拼音, 1消费 2抵扣 5折扣 7消费折扣 8红包
    '''
    table_id = SeparateDbTable(ssoid).get_vou_table()
    vou_key = str(vou_key)
    if vou_key.isdigit():
        if len(vou_key) > 2:            
            vou_id = vou_key    #vou_key是vouId
        else:            
            vou_type = vou_key  #vou_key是数字形式的vou_type
    else:        
        vou_type = voucher_type_enum[vou_key]   #vou_key是中文、英文形式的vou_type
    sql = "SELECT * FROM oppopay_voucher.vou_info_{} WHERE ssoid='{}' AND expireTime>=CURRENT_TIMESTAMP AND `status`=0 AND appId={} {} {} ORDER BY id DESC"\
          .format(table_id, ssoid, partner_id,
                  'AND type='+vou_type if locals().get('vou_type') else '',
                  "AND vouId='{}'".format(vou_id) if locals().get('vou_id') else '')
    result = GlobalVar.MYSQL_IN.select(sql)
    if len(result) > 1:
        return random.choice(result)
    return result[0]


def clear_all_unuseable_vou(ssoid, partner_id='2031'):
    '''
    清除所有失效的券
    :param ssoid:
    :param partner_id:
    '''
    table_id = SeparateDbTable(ssoid).get_vou_table()
    sql = "DELETE FROM oppopay_voucher.vou_info_{} WHERE ssoid='{}' AND appId='{}' AND `status`!=0".format(table_id, ssoid, partner_id)
    result = GlobalVar.MYSQL_IN.select(sql)


def get_renew_product_code(partner_id):
    sql = 'SELECT autorenew_product_code FROM platform_opay.autorenew_merchant_info WHERE partner_code="{}"'.format(partner_id)
    result = GlobalVar.MYSQL_IN.select_one(sql)
    if result:
        return result['autorenew_product_code']
    else:
        raise MySQLError('{} related renew_product_code is not configured'.format(partner_id))


if __name__ == '__main__':
#     print(get_balance("2076075925"))
    # print(get_balance("2076075925", country="VN", in_out="oversea"))
    # oversea_get_coin_rate("VND")
    #update_sign_status("2076075925", "wxpay")
#     print(get_ssoid_by_pay_req_id("RM202103031255262076075925123382"))
#     print(get_notify_id_by_request_id("RM202103031255262076075925123382"))
    pass
#     set_global_env_id(1)
#     _drop_spec_columns_on_all_order_tables('voucher_status', 'kebi_status', 'channel_status')
#     _add_columns_on_all_order_tables('voucher_status', 'kebi_status', 'channel_status')
