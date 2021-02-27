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
import unittest
logger = Logger('FizAssert').get_logger()


class FizAssert(unittest.TestCase, metaclass=WithLogger):
    def __init__(self, in_out="inland"):
        self.in_out = in_out
        self.mysql = GlobarVar.MYSQL_IN
        self.mysql_out = GlobarVar.MYSQL_OUT
        self._type_equality_funcs = {}

    def assert_order_info(self, ssoid, pay_req_id, amount, original_amount, kb_spent=0, vou_amount=0, vou_id=None):
        db_order_info = SeparateDbTable(ssoid).get_order_db_table()
        order_info = {}
        sql_oder = str(Config(common_sql_path).read_config("order", "order")).format(
            db_order_info[0], db_order_info[1], ssoid, pay_req_id)
        if self.in_out == "inland":
            order_info = self.mysql.select_one(sql_oder)
        if self.in_out == "oversea":
            order_info = self.mysql_out.select_one(sql_oder)
        self.logger.info("订单详情：{}".format(order_info))
        try:
            self.assertIsNotNone(order_info)
            self.assertEqual(order_info['amount'], amount)
            self.assertEqual(order_info['original_amount'], original_amount)
            self.assertEqual(order_info['status'], "OK")
            self.assertEqual(order_info['kebi_spent'], kb_spent)
            assert order_info['voucher_amount'] == vou_amount
            # 海外与国内订单表不一致，海外无该字段
            if self.in_out == "inland":
                assert order_info['voucher_id'] == vou_id
            self.logger.info("订单表信息记录正确")
        except AssertionError as e:
            self.logger.info("订单表信息记录异常")
            raise e

    def assert_trade_order(self, ssoid, pay_req_id, amount, original_amount, kb_amount=0, vou_amount=0):
        db_trade_order_info = SeparateDbTable(ssoid).get_order_db_table()
        trade_order_info = self.mysql.select_one(
            str(Config(common_sql_path).read_config("trade_order", "order")).format(
                db_trade_order_info[0], db_trade_order_info[1], ssoid, pay_req_id))
        self.logger.info("trade订单详情：{}".format(trade_order_info))
        try:
            self.assertIsNotNone(trade_order_info)
            self.assertEqual(trade_order_info['amount'], amount)
            self.assertEqual(trade_order_info['origin_amount'], original_amount)
            self.assertEqual(trade_order_info['status'], "OK")
            self.assertEqual(trade_order_info['kb_amount'], kb_amount)
            self.assertEqual(trade_order_info['voucher_amount'], vou_amount)
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
        recharge_info = {}
        sql_recharge = str(Config(common_sql_path).read_config("virtual", "recharge")).format(
                datetime.now().strftime("%Y%m"), ssoid, pay_req_id)
        if self.in_out == "inland":
            recharge_info = self.mysql.select_one(sql_recharge)
        if self.in_out == "oversea":
            recharge_info = self.mysql_out.select_one(sql_recharge)
        self.logger.info("tb_recharge订单详情：{}".format(recharge_info))
        try:
            if flag:
                self.assertIsNotNone(recharge_info)
                self.assertEqual(recharge_info['amount'], amount)
                self.assertEqual(recharge_info['status'], "OK")
            else:
                self.assertIsNone(recharge_info)
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
        payments_info = {}
        sql_payment = str(Config(common_sql_path).read_config("virtual", "payment")).format(
            datetime.now().strftime("%Y%m"), ssoid, partnerOrder)
        if self.in_out == "inland":
            payments_info = self.mysql.select_one(sql_payment)
        if self.in_out == "oversea":
            payments_info = self.mysql_out.select_one(sql_payment)
        self.logger.info("tb_payment订单详情：{}".format(payments_info))
        try:
            if flag:
                self.assertIsNotNone(payments_info)
                self.assertEqual(payments_info['price'], amount)
                self.assertEqual(payments_info['status'], "OK")
            else:
                self.assertIsNone(payments_info)
            self.logger.info("tb_payment订单表信息记录正确")
        except AssertionError as e:
            self.logger.info("tb_payment订单表信息记录正确")
            raise e

    def assert_notify(self, request_id):
        """
        :param request_id: 商户订单号
        :return:
        """
        notify_info = {}
        sql_notify = str(Config(common_sql_path).read_config("notify", "notify_info")).format(request_id)
        if self.in_out == "inland":
            notify_info = self.mysql.select_one(sql_notify)
        if self.in_out == "oversea":
            notify_info = self.mysql_out.select_one(sql_notify)
        self.logger.info("通知表信息详情：{}".format(notify_info))
        try:
            self.assertIsNotNone(notify_info)
            self.assertIn(notify_info['notify_response'], "OK", "ABANDON")
            if notify_info['notify_response'] == "OK":
                self.assertEqual(notify_info['notify_count'], 1)
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
        sign_status = self.mysql.select_one(
            str(Config(common_sql_path).read_config("order", "sign_status")).format(ssoid, partner_code,
                                                                                    renew_product_code, pay_type))
        try:
            self.assertIsNotNone(sign_status)
            self.assertEqual(sign_status['status'], "SIGN")
            self.logger.info("签约信息表记录正确")
        except AssertionError as e:
            self.logger.info("签约信息表记录异常")
            raise e

    def assert_auto_renew_sign_record(self, pay_req_id):
        """

        :return:
        """
        sign_record_status = self.mysql.select_one(
            str(Config(common_sql_path).read_config("order", "sign_record_status")).format(pay_req_id))
        try:
            self.assertIsNotNone(sign_record_status)
            self.assertEqual(sign_record_status['status'], "SUCC")
            self.logger.info("签约记录表记录正确")
        except Exception as e:
            self.logger.info("签约记录表记录异常")
            raise e

    def assert_voucher(self, ssoid, vou_id, status="6"):
        """
        检查优惠券状态
        :return:
        """
        table = SeparateDbTable(ssoid).get_vou_table()
        vou_info = {}
        sql_vou = str(Config(common_sql_path).read_config("voucher", "voucher_info")).format(table, vou_id)
        if self.in_out == "inland":
            vou_info = self.mysql.select_one(sql_vou)
        if self.in_out == "oversea":
            vou_info = self.mysql_out.select_one(sql_vou)
        self.logger.info("优惠券详情：{}".format(vou_info))
        try:
            self.assertIsNotNone(vou_info)
            self.assertEqual(vou_info['status'], status)
            self.logger.info("优惠券表记录正确")
        except Exception as e:
            self.logger.info("优惠券表记录异常")
            raise e
