#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/12 14:38
# comment:

import time
import base64
import binascii
from lib.interface_biz.dubbo.near_me import Nearme
from lib.interface_biz.dubbo.vou import Voucher
from lib.common.session.http.http_json import EncryptJson, HttpJsonSession
from lib.common.utils.globals import GlobarVar
from lib.common.utils.env import set_global_env_id
from lib.interface_biz.http.refund import Refund
from lib.common.algorithm.aes import AES_CBC
import chardet


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

#     # http自动退款
#     session = None
#     env_id = 'product'
#     if env_id == 'grey':
#         session = HttpJsonSession('https://pre-nativepay.keke.cn')  # 灰度域名
#     elif env_id == 'product':
#         session = HttpJsonSession('https://nativepay.keke.cn')  # 正式域名
#     set_global_env_id(env_id)
#     refund = Refund('2086100900', http_session=session or GlobarVar.HTTPJSON_IN)   # 14213467928
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
    exp = 'g1f0ecbjsm/94OZ1cJ2Fo8HLPaYl6n+58oNBz+PS+HRhSxMd2KhIvcVV+w8T5zXHqJy/KZfM2Rq5V+ZOPEugC8RTxwi4uSkTA+k7RaneHMLgsOw0negWYWR01GAMWWh3rHDXA1N8heL+Iy1FtGZTH/5kG+sxmvv6KQ7l+HAwgUbAVHSnmvwWxr95TBzaf6FIoxA='
    text = '{"imei":"","mac":"0","serialNum":"unknown","serial":"unknown","hasPermission":true,"wifissid":"<unknown ssid>","deviceName":"PEDM00","slot1":"{}"}'
    print('原文：', text)
    base64_iv = 'QxbF3LonVTkM9UxJkoysmQ=='
    bytes_iv = base64.b64decode(base64_iv)
    aes_cbc = AES_CBC('FsZtyBxlB_oTcrXQ7kiYDQ==', bytes_iv)
    res = aes_cbc.encrypt_and_base64(text)
    
    print('开始解密')
#     x = binascii.b2a_base64(base64.b64decode(exp)).strip(b'\n')
#     print('base64解密之后：', x)
    x = base64.b64decode(exp)   # decode base64
    print('base64解密之后：', x)
    print('aes解密之后：', aes_cbc.decrypt(x))
    
    '''
    base64.b64encode(bytesString) & b2a_base64(bytesString) 功能一致       
    base64.b64decode(encodestr) & a2b_base64(encodestr) 功能一致
    '''
    
#     # pb2json 加密传输新协议
#     set_global_env_id(3)
#     encjson = EncryptJson(GlobarVar.URL_PAY_IN)
#     encjson.post('/api/conf/v1/service-base-info', {'partnerId': '2031'})
    
    
