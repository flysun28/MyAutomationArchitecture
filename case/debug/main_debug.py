#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/12 14:38
# comment:

import time
import base64
import binascii

from lib.common_biz.find_database_table import SeparateDbTable
from lib.interface_biz.dubbo.near_me import Nearme
from lib.interface_biz.dubbo.vou import Voucher
from lib.common.session.http.http_json import EncryptJson, HttpJsonSession
from lib.common.utils.globals import GlobalVar
from lib.common.utils.env import set_global_env_id
from lib.interface_biz.http.refund import Refund
from lib.common.algorithm.aes import AES_CBC
import chardet
from lib.interface_biz.scarlett.oversea_coda import coda_pay


if __name__ == '__main__':
#     # http自动退款
#     session = None
#     env_id = 'product'
#     if env_id == 'grey':
#         session = HttpJsonSession('https://pre-nativepay.keke.cn')  # 灰度域名
#     elif env_id == 'product':
#         session = HttpJsonSession('https://nativepay.keke.cn')  # 正式域名
#     set_global_env_id(env_id)
#     refund = Refund('2086100900', http_session=session or GlobalVar.HTTPJSON_IN)   # 14213467928
#     per_amount = 0.01
#     total_amount = 0.01
#     loop_num = int(total_amount/per_amount)
#     for i in range(loop_num):

#         while True:
#             response = refund.httpjson_refund('136e769358dc4591ad7bbadad90604ec', '2031', per_amount, pay_req_id='')
#             if response['resMsg'] == '退款失败':
#                 time.sleep(1)
#             else:
#                 break
#
#     flag_coin = "1"
#     if flag_coin == "1":
#         # 发
#         Nearme().nearme_add_subtract("10", "2076075925", 0)
#     if flag_coin == "2":
#         # 扣
#         Nearme().nearme_add_subtract("5", "2076075925", 1)
# 
    flag = "4"
#     if flag == "1":
#         # 满减
#         vou_info = Voucher().grantVoucher("2031", "KB_COUPON", "DIKOU", "10", "9.99", "2076075925")
#         Voucher().checkVoucher(vou_info['batchId'])
#         # 消费
#     if flag == "2":
#         vou_info = Voucher().grantVoucher("2031", "KB_COUPON", "XIAOFEI", "0", "10", "2076075925")
#         Voucher().checkVoucher(vou_info['batchId'])X
#     if flag == "3":
#         # 红包券
#         vou_info = Voucher().grantVoucher("5456925", "KB_COUPON", "RED_PACKET_COUPON", "0", "10", "2076075925")
#         Voucher().checkVoucher(vou_info['batchId'])
    if flag == "4":
        # 海外满减
        vou_info = Voucher("oversea").grantVoucher("5456925", "KB_COUPON", "DIKOU", "5000", "1000", "2076075925", "IN",
                                                   "INR")
        Voucher("oversea").checkVoucher(vou_info['batchId'])

    coda_pay("10000.00", "390", "", "IN202104020907322076075925462453", "1c3d4a652f744f340e7ad9471dbdcb5d")
    # print(SeparateDbTable("2086762813").get_order_db_table())