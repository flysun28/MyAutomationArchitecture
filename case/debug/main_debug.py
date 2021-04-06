#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/12 14:38
# comment:
env_id = '3'
from lib.common.utils.env import set_global_env_id
set_global_env_id(env_id)

import os
import time
import base64
import binascii

import string
import random
import requests
from itertools import chain
from concurrent.futures import ALL_COMPLETED, wait
from concurrent.futures.thread import ThreadPoolExecutor
from lib.common.utils.misc_utils import create_random_str
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
    pass
#     flag_coin = "1"
#     if flag_coin == "1":
#         # 发
#         Nearme().nearme_add_subtract("10", "2076075925", 0)
#     if flag_coin == "2":
#         # 扣
#         Nearme().nearme_add_subtract("5", "2076075925", 1)
# 
#     flag = "4"
#     if flag == "1":
#         # 满减
#         vou_info = Voucher().grantVoucher("2031", "KB_COUPON", "DIKOU", "10", "9.99", "2076075925")
#         Voucher().checkVoucher(vou_info['batchId'])
#         # 消费
#     if flag == "2":
#         vou_info = Voucher().grantVoucher("2031", "KB_COUPON", "XIAOFEI", "0", "10", "2076075925")
#         Voucher().checkVoucher(vou_info['batchId'])
#     if flag == "3":
#         # 红包券
#         vou_info = Voucher().grantVoucher("5456925", "KB_COUPON", "RED_PACKET_COUPON", "0", "10", "2076075925")
#         Voucher().checkVoucher(vou_info['batchId'])
#     if flag == "4":
#         # 海外满减
#         vou_info = Voucher("oversea").grantVoucher("9809089", "KB_COUPON", "DIKOU", "10000", "7500", "2076075925", "VN",
#                                                    "VND")
#         Voucher("oversea").checkVoucher(vou_info['batchId'])

#     # 审批退款
#     refund = GrantRefund("2086100900")
#     refund.refund_by_pay_req_id('RM202103251132432086100900173732')

#     # http自动退款
#     session = None
#     env_id = 'product'
#     if env_id == 'grey':
#         session = HttpJsonSession('https://pre-nativepay.keke.cn')  # 灰度域名
#     elif env_id == 'product':
#         session = HttpJsonSession('https://nativepay.keke.cn')  # 正式域名
#     refund = HttpRefund('2086100900', http_session=session or GlobalVar.HTTPJSON_IN)   # 14213467928
#     per_amount = 35
#     total_amount = 35
#     loop_num = int(total_amount/per_amount)
#     for i in range(loop_num):

#         while True:
#             response = refund.httpjson_refund('GC202103291303557330900240000', '5456925', per_amount, pay_req_id='')
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
#     if flag == "4":
#         # 海外满减
#         vou_info = Voucher("oversea").grantVoucher("5456925", "KB_COUPON", "DIKOU", "5000", "1000", "2076075925", "IN",
#                                                    "INR")
#         Voucher("oversea").checkVoucher(vou_info['batchId'])

    coda_pay("9500.00", "390", "", "IN202104040305312076075925776873", "1c3d4a652f744f340e7ad9471dbdcb5d")
    # print(SeparateDbTable("2086762813").get_order_db_table())
#     base64_iv = 'VHl2UW1oWUlqM25lcEx1cw=='
#     bytes_iv = base64.b64decode(base64_iv)
#     aes_cbc = AES4J('8i_Dq8KHbCtGm9mjQWcx4A==', bytes_iv)
# #     aes_cbc = AES_CBC('NE90SWF2bU0xa1c3Y1FmaQ==', bytes_iv)
#      
#     print('开始解密')
#     x = 'ZjFiMDRjMmRjYWM5ZjdhYzg5ZTIyY2M0NTNjNDkyZDYyZTUyYzdiODZlZWEzMWI0MzVlZDJlMDhmNzZjZGU5NTYxYTMxMDMyYTI2MTllN2YyNTYwMGEwOWY3OTFiYzAzY2U3ZDcxMWM2YTllYjBjNWNjOGU5M2ZkZGQ1MmUwYzY2M2E0YjMyZDBhYjFkMjQ0MDlkMGY3YjZmNzFjZjM1MDAzNjg2M2RjODIwMWMyZjZiMDEwY2QxODM1Yjc5MThhMGIzZmNhYThiZGQ0N2U5YzczMjBhY2VkM2EwZTlmYTgxZTFiMmZmOTQ5NzVkZjZmMThlOGUwODBjYmM1YWM0ZjBkMGZjNzY0NjE0N2FhNDFjMzlkYzRmY2E5ZjE2ZmNl'
#     y = aes_cbc.decrypt(x)
#     print('aes解密之后：', y)    
#     z = aes_cbc.encrypt('{"appKey": "2033","position": "result_page","nonce": "12345678","timestamp": "1612670150","partnerId": "5456925","bizId": "BN1022","sign": "bdf1aea649bddee826c0a36909a391b5"}')
#     print(z)
   
    # pb2json 加密传输新协议
    # encjson = EncryptJson(GlobalVar.URL_PAY_IN)
    # result = encjson.post('/api/conf/v1/service-base-info', {'partnerId': '2031'})
    # print(result['data']['contactInfo'])
    # result = encjson.post('/api/conf/v1/package-name', {})
    # print(result['data']['walletPackageName'])

