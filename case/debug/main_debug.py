#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/12 14:38
# comment:
env_id = '2'
from lib.common.utils.env import set_global_env_id
set_global_env_id(env_id)

import os
import time
import base64
import binascii
import string
import random
from multiprocessing.pool import ThreadPool
from concurrent.futures import ALL_COMPLETED, FIRST_COMPLETED, wait
from concurrent.futures.thread import ThreadPoolExecutor
from lib.common.utils.misc_utils import create_random_str
from lib.common_biz.find_database_table import SeparateDbTable
from lib.interface_biz.dubbo.near_me import Nearme
from lib.interface_biz.dubbo.vou import Voucher
from lib.common.session.http.http_json import EncryptJson, HttpJsonSession
from lib.common.utils.globals import CASE_SRCFILE_ROOTDIR, GlobalVar
from lib.interface_biz.http.refund import Refund as HttpRefund
from case.debug.inland.dubbo.refund import Refund as GrantRefund
from lib.common.algorithm.aes import AES_CBC
from lib.interface_biz.http.grant_voucher import VouInfo, HttpGrantMultiVous



if __name__ == '__main__':
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
#     per_amount = 15
#     total_amount = 15
#     loop_num = int(total_amount/per_amount)
#     for i in range(loop_num):
#         while True:
#             response = refund.httpjson_refund('GC202103281341480020900220000', '5456925', per_amount, pay_req_id='')
#             if response['resMsg'] == '退款失败':
#                 time.sleep(1)
#             else:
#                 break

#     exp = 'g1f0ecbjsm/94OZ1cJ2Fo8HLPaYl6n+58oNBz+PS+HRhSxMd2KhIvcVV+w8T5zXHqJy/KZfM2Rq5V+ZOPEugC8RTxwi4uSkTA+k7RaneHMLgsOw0negWYWR01GAMWWh3rHDXA1N8heL+Iy1FtGZTH/5kG+sxmvv6KQ7l+HAwgUbAVHSnmvwWxr95TBzaf6FIoxA='
#     text = '{"imei":"","mac":"0","serialNum":"unknown","serial":"unknown","hasPermission":true,"wifissid":"<unknown ssid>","deviceName":"PEDM00","slot1":"{}"}'
#     print('原文：', text)
#     base64_iv = 'QxbF3LonVTkM9UxJkoysmQ=='
#     bytes_iv = base64.b64decode(base64_iv)
#     aes_cbc = AES_CBC('FsZtyBxlB_oTcrXQ7kiYDQ==', bytes_iv)
# #     res = aes_cbc.encrypt_and_base64(text)
#     
#     print('开始解密')
# #     x = binascii.b2a_base64(base64.b64decode(exp)).strip(b'\n')
# #     print('base64解密之后：', x)
#     x = base64.b64decode(exp)   # decode base64
#     print('base64解密之后：', x)
#     y = aes_cbc.decrypt(x)
#     print('aes解密之后：', y)
#     z = 
    
   
#     # pb2json 加密传输新协议
#     set_global_env_id(3)
#     encjson = EncryptJson(GlobalVar.URL_PAY_IN)
#     encjson.post('/api/conf/v1/service-base-info', {'partnerId': '2031'})
    
    # 批量发券正常测试
    case_file_path = os.path.join(CASE_SRCFILE_ROOTDIR, 'http', 'inland.xlsx')
    vouinfo = VouInfo(case_file_path)
    vouinfo.create()
#     httpmultivou = HttpGrantMultiVous(vouinfo, '2086100900', '2031')
#     httpmultivou.post()
    all_tasks = []
    executor = ThreadPoolExecutor(max_workers=200)
    for ssoid in '2086100900', '2086628989', '2000062087':
        SeparateDbTable(ssoid).get_vou_table()
        httpmultivou = HttpGrantMultiVous(vouinfo, ssoid, '2031')
        [all_tasks.append(executor.submit(httpmultivou.post)) for i in range(executor._max_workers)]
    wait(all_tasks, return_when=ALL_COMPLETED)
    # 批量发券异常测试
    ########################################### 负向测试参数列表 Start ###########################################
    '异常测试受限：长度越界会自动截断，非str会转换为str类型'
    rand_str_65 = ''.join(random.sample(string.ascii_letters+string.digits, 33))*2
    ssoids = '2086100900', '', #rand_str_65
    countries = 'CN', '',  #rand_str_65
    timezones = 'GMT+08:00', '', #rand_str_65
    currencies = 'CNY', '', #rand_str_65
    appids = '2031', '', #rand_str_65
    partner_orders = create_random_str(62), '', rand_str_65
    ########################################### 负向测试参数列表 End   ###########################################
#     httpmultivou.common_params_negative_test(ssoid=ssoids, country=countries, timezone=timezones, currency=currencies, appId=appids, requestId=partner_orders)
    
    ########################################### 负向测试参数列表 Start ###########################################
    voutypes = '1', 5*'a', -1000, 
    names = 'CN', 11111, '', -1.234, 5*'a'
    grantCounts = 1, 0, 
    amounts = 1.234, '', 5*'a', 9999999999.999
    maxAmounts = 9999999999.99, '2031', '', -1.234, 9999999999.999, 10000000000
    ratios = 0.999, 10000000000, '', -1.234
    beginTimes = 1, 0, -1, 2**32+1, ''
    expireTimes = 1, 0, -1, 2**32+1, ''
    scopeIds = 'a', ''
    subScopeIds = '',
    blackScopeIds = 'b',
    settleTypes = 1, -1, 'a', ''
    batchIds = 'a', 0, ''
    ########################################### 负向测试参数列表 End   ###########################################
#     httpmultivou.vouinfolist_negative_test(vouType=voutypes, vouName=names, grantCount=grantCounts, amount=amounts, maxAmount=maxAmounts, ratio=ratios, beginTime=beginTimes, expireTime=expireTimes, scopeId=scopeIds, subScopeId=subScopeIds, blackScopeId=blackScopeIds, settleType=settleTypes, batchId=batchIds)

