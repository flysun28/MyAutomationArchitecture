#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 22:54
# comment: 业务分库分表查询
import re

from lib.common.algorithm.hash_code import GetHashCode
from lib.common.utils.meta import WithLogger


def get_route_ssoid(ssoid):
    """
    ssoid>=10位时，截取后10位数
    ssoid<10位数时，ssoid = n位0+ssoid，补齐到10位
    :param ssoid:
    :return:
    """
    if len(ssoid) >= 10:
        ssoid = ssoid[len(ssoid) - 10:]
    else:
        ssoid = (10 - len(ssoid)) * str(0) + ssoid
    return ssoid

def get_ssoid_by_pay_req_id(pay_req_id):
    return str(pay_req_id)[16: 26]


class SeparateDbTable(metaclass=WithLogger):
    def __init__(self, ssoid):
        self.ssoid = ssoid

    def get_order_db_table(self):
        """
        order-info表/tradeorder表，分库分表
        :param ssoid:
        :return:
        """
        hash_code = abs(GetHashCode.getHashCode(self.ssoid))
        db = int(hash_code / 128 % 8)
        table = hash_code % 128
        # self.logger.info("`db_order_{}`.`order_info_{}`".format(db, table))
        return db, table

    def get_coin_db_table(self):
        """
        可币用户信息分库分表
        :return:
        """
        hash_code = abs(GetHashCode.getHashCode(self.ssoid))
        temp = int(hash_code / 256)
        db = temp % 4
        table = hash_code % 256
        self.logger.info("`pay_cocoin_{}`.`pay_user_info_{}`".format(db, table))
        return db, table

    def get_coin_order_db_table(self):
        """
        可币订单分库分表
        :return:
        """
        db_count = 4
        table_count = 1024
        temp = int(abs(GetHashCode.getHashCode(self.ssoid)) / table_count)
        data_base = temp % db_count
        table = int(abs(GetHashCode.getHashCode(self.ssoid)) % table_count)
        # self.logger.info("`pay_cocoin_{}`.`pay_cocoin_order_{}`".format(data_base, table))
        return data_base, table

    def get_vou_table(self):
        """
        优惠券分库分表
        :return:
        """
        count = 20
        table = int(abs(GetHashCode.getHashCode(self.ssoid))) % count + 1
        self.logger.info("`oppopay_voucher`.`vou_info_{}`".format(table))
        return table

    def get_user_type_db_table(self):
        """
        用户上次成功支付的支付方式
        :return:
        """
        db_count = 2
        table_count = 128
        userId = re.sub("^0*", "", get_route_ssoid(self.ssoid))
        temp = int(abs(GetHashCode.getHashCode(userId)) / table_count)
        table = int(abs(GetHashCode.getHashCode(userId))) % table_count
        db = temp % db_count
        # self.logger.info("`db_user_paytype_{}`.`user_paytype_{}`".format(db, table))
        return db, table


if __name__ == '__main__':
#     print(SeparateDbTable("490481564").get_order_db_table())
    print(SeparateDbTable("2076074648").get_order_db_table())
#     print(SeparateDbTable("2076075925").get_user_type_db_table())
    print(SeparateDbTable("2076074648").get_vou_table())
#     print(SeparateDbTable("2076074648").get_coin_db_table())
#     print(SeparateDbTable("2086788561").get_vou_table())