#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/18 16:39
# comment:
from datetime import datetime
from lib.common.file_operation.config_operation import Config
from lib.common.logger.logging import Logger
from lib.common.utils.globals import GlobarVar
from lib.common.utils.meta import WithLogger
from lib.common_biz.find_database_table import SeparateDbTable
from lib.config.path import common_sql_path
logger = Logger('FizAssert').get_logger()


class FizAssert(metaclass=WithLogger):
    def __init__(self):
        self.mysql = GlobarVar.MYSQL_IN

    def assert_order_info(self, ssoid, pay_req_id, amount, original_amount, kb_spent=0, vou_amount=0, vou_id=None):
        db_order_info = SeparateDbTable(ssoid).get_order_db_table()
        order_info = self.mysql.select_one(
            str(Config(common_sql_path).read_config("order", "order")).format(db_order_info[0], db_order_info[1], ssoid,
                                                                              pay_req_id))
        self.logger.info("订单详情：{}".format(order_info))
        try:
            assert order_info is not None
            assert order_info['amount'] == amount
            assert order_info['original_amount'] == original_amount
            assert order_info['status'] == "OK"
            assert order_info['kebi_spent'] == kb_spent
            assert order_info['voucher_amount'] == vou_amount
            assert order_info['voucher_id'] == vou_id
            self.logger.info("订单表信息记录正确")
        except AssertionError as e:
            self.logger.info("订单表信息记录异常")
            raise e

    def assert_trade_order(self, ssoid, pay_req_id, amount, original_amount, kb_amount=0, vou_amount=0):
        db_trade_order_info = SeparateDbTable(ssoid).get_order_db_table()
        trade_order_info = self.mysql.select_one(
            str(Config(common_sql_path).read_config("trade_order", "order")).format(db_trade_order_info[0],
                                                                              db_trade_order_info[1], ssoid,
                                                                              pay_req_id))
        self.logger.info("trade订单详情：{}".format(trade_order_info))
        try:
            assert trade_order_info is not None
            assert trade_order_info['amount'] == amount
            assert trade_order_info['origin_amount'] == original_amount
            assert trade_order_info['status'] == "OK"
            assert trade_order_info['kb_amount'] == kb_amount
            assert trade_order_info['voucher_amount'] == vou_amount
            self.logger.info("trade订单表信息记录正确")
        except AssertionError as e:
            self.logger.info("trade订单表信息记录异常")
            raise e

    def assert_tb_recharge(self, ssoid, pay_req_id, amount, flag=True):
        """
        :param flag: 当为true, 表记录不能为空 assert trade_order_info is not None
        :param ssoid:
        :param pay_req_id:
        :param amount:
        :return:
        """
        recharge_info = self.mysql.select_one(
            str(Config(common_sql_path).read_config("virtual", "recharge")).format(datetime.now().strftime("%Y%m"),
                                                                                   ssoid, pay_req_id))
        self.logger.info("tb_recharge订单详情：{}".format(recharge_info))
        try:
            if flag:
                assert recharge_info is not None
                assert recharge_info['amount'] == amount
                assert recharge_info['status'] == "OK"
            else:
                assert recharge_info is None
            self.logger.info("tb_recharge订单表信息记录正确")
        except AssertionError as e:
            self.logger.info("tb_recharge订单表信息记录异常")
            raise e

    def assert_tb_payment(self, ssoid, partnerOrder, amount, flag=True):
        """
        :param flag: 当为true, 表记录不能为空 assert trade_order_info is not None
        :param ssoid:
        :param partnerOrder: 商户订单号
        :param amount:
        :return:
        """
        payments_info = self.mysql.select_one(str(Config(common_sql_path).read_config("virtual", "payment")).
                                              format(datetime.now().strftime("%Y%m"), ssoid, partnerOrder))
        self.logger.info("tb_payment订单详情：{}".format(payments_info))
        try:
            if flag:
                assert payments_info is not None
                assert payments_info['price'] == amount
                assert payments_info['status'] == "OK"
            else:
                assert payments_info is None
            self.logger.info("tb_payment订单表信息记录正确")
        except AssertionError as e:
            self.logger.info("tb_payment订单表信息记录正确")
            raise e

    def assert_notify(self, request_id):
        """
        :param request_id: 商户订单号
        :return:
        """
        notify_info = self.mysql.select_one(str(Config(common_sql_path).read_config("notify", "notify_info")). format(
                                                                                                            request_id))
        self.logger.info("通知表信息详情：{}".format(notify_info))
        try:
            assert notify_info is not None
            assert notify_info['notify_response'] == "OK"
            assert notify_info['notify_count'] == 1
            self.logger.info("通知成功")
        except AssertionError as e:
            self.logger.info("通知异常")
            raise e

    def assert_auto_renew_sign_info(self, ssoid, pay_type, partner_code="2031", renew_product_code="20310001"):
        """

        :param ssoid:
        :param pay_type:
        :param partner_code:
        :param renew_product_code:
        :return:
        """
        sign_status = self.mysql.select_one(str(Config(common_sql_path).read_config("order", "sign_status")). format(ssoid, partner_code, renew_product_code, pay_type))
        try:
            assert sign_status is not None
            assert sign_status['status'] == "SIGN"
            self.logger.info("签约信息表记录正确")
        except AssertionError as e:
            self.logger.info("签约信息表记录异常")
            raise e

    def assert_auto_renew_sign_record(self, pay_req_id):
        """

        :return:
        """
        sign_record_status = self.mysql.select_one(str(Config(common_sql_path).read_config("order", "sign_record_status")). format(pay_req_id))
        try:
            assert sign_record_status is not None
            assert sign_record_status['status'] == "SUCC"
            self.logger.info("签约记录表记录正确")
        except Exception as e:
            self.logger.info("签约记录表记录异常")
            raise e