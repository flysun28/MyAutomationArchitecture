#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/12 14:38
# comment:
from lib.common.file_operation.excel_operation import Excel
from lib.common.utils.env import set_global_env_id
from lib.interface_biz.dubbo.near_me import Nearme
from lib.interface_biz.dubbo.vou import Voucher
from lib.interface_biz.scarlett.heepay import hee_pay_notify

if __name__ == '__main__':
    # set_global_env_id(3)
    # hee_pay_notify("KB202103151434522076075925533222", 10000, "574A4702E0644DA29E827E05", bill_status="1")
    #
    # # 可币和优惠券
    # kb_or_vou = 1
    # flag_coin = "1"
    # flag_vou = "2"
    # if kb_or_vou == 1:
    #     if flag_coin == "1":
    #         # 发
    #         Nearme().nearme_add_subtract("10", "2076075925", 0)
    #     if flag_coin == "2":
    #         # 扣
    #         Nearme().nearme_add_subtract("10", "2076075925", 1)
    #
    # if kb_or_vou == 2:
    #     if flag_vou == "1":
    #         # 满减
    #         vou_info = Voucher().grantVoucher("2031", "KB_COUPON", "DIKOU", "10", "9.99", "2076075925")
    #         Voucher().checkVoucher(vou_info['batchId'])
    #         # 消费
    #     if flag_vou == "2":
    #         vou_info = Voucher().grantVoucher("5456925", "KB_COUPON", "XIAOFEI", "0", "10", "2076075925")
    #         Voucher().checkVoucher(vou_info['batchId'])
    #     if flag_vou == "3":
    #         # 红包券
    #         vou_info = Voucher().grantVoucher("5456925", "KB_COUPON", "RED_PACKET_COUPON", "0", "10", "2076075925")
    #         Voucher().checkVoucher(vou_info['batchId'])
    #     if flag_vou == "4":
    #         # 海外满减
    #         vou_info = Voucher("oversea").grantVoucher("9809089", "KB_COUPON", "DIKOU", "10000", "7500", "2076075925", "VN",
    #                                                    "VND")
    #         Voucher("oversea").checkVoucher(vou_info['batchId'])
    pass