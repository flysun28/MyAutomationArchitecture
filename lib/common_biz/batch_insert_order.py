#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/7/22 21:18
# comment:
from lib.common.utils.globals import GlobalVar
from lib.common_biz.find_database_table import SeparateDbTable
import time

from lib.common_biz.order_random import RandomOrder

mysql = GlobalVar.MYSQL_IN


def insert_order(ssoid, amount, partner_id):
    time_now = time.strftime("%Y%m%d%H%M%S")
    time_str_time = time.strftime("%Y-%m-%d %H:%M:%S")
    db_info = SeparateDbTable("2086793483").get_order_db_table()
    db = db_info[0]
    table = db_info[1]
    sql = "INSERT INTO `db_order_{}`.`order_info_{}` (`id`, `pay_req_id`, `notify_id`, `partner_order`, `amount`, " \
          "`refund`, `contents`, `products_name`, `counts`, `ssoid`, `mobile_num`, `imei`, `imsi`, `imsi2`, `ip`, " \
          "`mac`, `model`, `app_package`, `app_ver`, `sdk_ver`, `partner_code`, `notify_url`, `status`, `channel_id`, " \
          "`channel_type`, `pay_type`, `direct_pay`, `game_type`, `present_amount`, `original_amount`, `discount_info`," \
          " `extra`, `remark`, `request_time`, `success_time`, `modify_time`, `trade_type`, `kebi_spent`, " \
          "`voucher_amount`, `voucher_info`, `country_code`, `currency`, `openid`, `brand_type`, `mobile_os_ver`, " \
          "`platform`, `screen_info`, `voucher_id`, `factor`, `paid_amount`, `paid_usd`, `combine_order`, " \
          "`voucher_status`, `kebi_status`, `channel_status`, `profit_sharing`, `credit_count`, " \
          "`credit_deduct_amount`, `credit_status`, `payment_type`) VALUES('0','{}','{}'," \
          "'{}','{}','0','充值并消费','充值并消费','1','{}',NULL," \
          "'867472038703651','000000000000000',NULL,'183.238.137.92','','PDRM00','com.example.pay_demo','1.1.0','280'," \
          "'{}','http://pay.pay-test.wanyol.com/notify/receiver','OK','qqwallet','NATIVE','qqwallet','KEBI'," \
          "'WANGYOU','0','10000','',NULL,'new way','{}','{}','{}'," \
          "'PAY','0','0','','CN','CNY','FA9F4EB109FB493B9F6F8469468B8861fd527ea65e79f18e75bd1f05132f1a2c','OPPO','20'," \
          "'','FULL','0','',NULL,NULL,'N',NULL,'OK','OK','N','0','0',NULL,'COMMON')".format(db, table, "KB" + time_now + ssoid + RandomOrder(6).random_num(),
                                    RandomOrder(32).random_num(),RandomOrder(32).random_num(), amount, ssoid, partner_id,
                                    time_str_time,time_str_time,time_str_time)
    mysql.execute(sql)


if __name__ == '__main__':
    for item in range(999):
        insert_order("2086793483", "10000", "5456925")