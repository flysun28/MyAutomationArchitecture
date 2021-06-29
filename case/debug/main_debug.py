# coding=utf-8
env_id = '3'
from lib.common.utils.env import set_global_env_id
set_global_env_id(env_id)

import os
import sys
import time
import base64
import binascii
import string
import random
import requests
from itertools import chain
from concurrent.futures import ALL_COMPLETED, wait
from concurrent.futures.thread import ThreadPoolExecutor
from lib.common.utils.misc_utils import create_random_str, extend_to_longest
from lib.common_biz.find_database_table import SeparateDbTable
from lib.interface_biz.dubbo.near_me import Nearme
from lib.interface_biz.dubbo.vou import Voucher
from lib.common.session.http.http_json import EncryptJson, HttpJsonSession
from lib.common.utils.globals import GlobalVar, CASE_SRCFILE_ROOTDIR, HTTPJSON_SCARLET
from lib.interface_biz.http.refund import Refund
from lib.interface_biz.dubbo.refund import Refund as GrantRefund
from lib.common.algorithm.aes import AES4J
from lib.common.exception.intf_exception import IgnoreException
from lib.interface_biz.http.grant_voucher import HttpGrantMultiVous, VouInfo, grant_single_voucher, HttpGrantSingleVous
from lib.common.db_operation.redis_operation import connect_redis
from lib.common.utils.descriptors import GlobalVarDescriptor
from lib.interface_biz.scarlett.alipay import ali_sign_scarlet, ali_sign_scarlet_by_raw_resp
from lib.interface_biz.scarlett.wxpay import wx_sign_scarlet
from lib.interface_biz.scarlett.map_to_json import scarlet_map_to_json
from case.debug.inland.json.auto_renew import AutoRenew as AutoRenewDebug
from lib.common_biz.fiz_assert import is_assert, ASSERTION_IN
from lib.common_biz.choose_scarlett import choose_scarlett
from lib.interface_biz.http.query_result import queryResult
from lib.interface_biz.dubbo.refactor.paycenter import PayCenterDubbo
from case.debug.inland.dubbo.voucher import VoucherInland
from lib.common_biz.biz_db_operate import get_available_voucher, get_renew_product_code
from lib.interface_biz.http.auto_re_new import AutoRenew


if __name__ == '__main__':
#     Nearme().query_balance('2086776969')    #pay_cocoin_3.pay_user_info_158
    flag_coin = "0"
    if flag_coin == "1":
        # 发
        Nearme().nearme_add_subtract("0.01", "2086776969", 0)
    if flag_coin == "2":
        # 扣
        Nearme().nearme_add_subtract("0.01", "2086776969", 1)
#     ssoid = '2086788561'    #黄勇翔
#     ssoid = '2076074648'    #黄小静
#     ssoid = '2076079836'    #陈华平
#     ssoid = '2086631885'    #彭哲
    partner_id = '2031'     #主题9809089
    ssoid = '2086776969'
    if env_id.isdigit():
        voucher = Voucher()
        for flag in range(2, 2):
            if flag == 1:
                # 满减(抵扣)
                voucher.grant_check_voucher(partner_id, "KB_COUPON", "DIKOU", "1", "0.99", ssoid)
            if flag == 2:
                # 消费
                for _ in range(10):
                    voucher.grant_check_voucher(partner_id, "KB_COUPON", "XIAOFEI", "0", "0.01", ssoid)
            if flag == 3:
                # 折扣
                voucher.grant_check_voucher(partner_id, "KB_COUPON", "DAZHE", "1", "0", ssoid, ratio=0.68, maxCutAmount='1')
#                 voucher.grant_check_voucher(partner_id, "KB_COUPON", "DAZHE", "1", "0", ssoid, ratio=0.1, maxCutAmount='1')
            if flag == 4:
                # 消费折扣
                voucher.grant_check_voucher(partner_id, "KB_COUPON", "XIAOFEI_DAZHE", "1", "0", ssoid, ratio=0.01, maxCutAmount='10')
            if flag == 5:
                # 红包券
                voucher.grant_check_voucher(partner_id, "KB_COUPON", "RED_PACKET_COUPON", "0", "1", ssoid)
            if flag == 6:
                # 海外满减
                Voucher("oversea").grant_check_voucher("5456925", "KB_COUPON", "DIKOU", "10000", "7500", "2076074648", "ID", "IDR")
                Voucher("oversea").grant_check_voucher("5456925", "KB_COUPON", "DAZHE", "10000", "0", "2076074648", "ID", "IDR", ratio=0.1, maxCutAmount='10000')
                Voucher("oversea").grant_check_voucher('5456925', "KB_COUPON", "XIAOFEI_DAZHE", "10000", "0", '2076074648', "ID", "IDR", ratio=0.2, maxCutAmount='10000')
    # 通过批次号审核券
#     VoucherInland().checkVoucher('a39a8a029ebc4055bdc9a489d9a765d5')

    # 查询优惠券
#     Voucher().query_voucher_by_id('2086776969', '62641621')
#     Voucher().query_all_useable('2086776969', partner_id='2031')

#     # 审批退款：order审批，dispatcher退款
    refund = GrantRefund("2086776969")
    refund.refund_by_pay_req_id('')
    refund.refund_by_amount('', amount=0.02)
    
    # http自动退款
    session = None
    if env_id == 'grey':
        session = HttpJsonSession('https://pre-nativepay.keke.cn')  # 灰度域名
    elif env_id == 'product':
        session = HttpJsonSession('https://nativepay.keke.cn')  # 正式域名
    refund = Refund('2086776969', http_session=session or GlobalVar.HTTPJSON_IN)   # 14213467928
    # 根据业务订单号退款
    per_amount = 0.01
    total_amount = 0
    loop_num = int(total_amount/per_amount)
    for i in range(loop_num):
        while True:
            response = refund.httpjson_refund('', '5456925', per_amount, pay_req_id='')
            if response['resMsg'] == '退款失败':
                time.sleep(1)
            else:
                break

    # 根据支付订单号退款
    refund.refund_by_pay_req_id('', 0.01)

#     # pb2json
#     base64_iv = 'V2NNQ2J2NUdGenV3TGFyNw=='
#     bytes_iv = base64.b64decode(base64_iv)
#     aes_cbc = AES4J('bEliWVVUZzR0RUhwSldvMg==', bytes_iv, '3.0')      
#     print('开始解密')
#     x = 'FuQ6X0zWO24Nno0btUr+JC9PXN+mXXUH+swbJAfIEZ/1erGTVlSPbN0YTwaPsVRwMcw0fw3/A/XCxbDEVFC/8cY0vt56cDrgT0ynM89ctMUCi5UxJGhtjE867W5C9Mr3rOFK4QZIOIFyv+gGH/YtUe+pYu1rI0jlMILR3qYe51jUpAAk1JS6FVnMTcGTo/DxmZrp0cBXJY+LSttDFxH/FQAi5VH/5dRezSlOh/jynFTVmDBOPw1/r/QA+SyC5dcUTSJ8Eb84/g=='
#     y = aes_cbc.decrypt(x)
#     print('aes解密之后：', y)
#     z = aes_cbc.encrypt('{"appKey": "2033","position": "result_page","nonce": "12345678","timestamp": "1612670150","partnerId": "5456925","bizId": "BN1022","sign": "bdf1aea649bddee826c0a36909a391b5"}')
#     print(z)

#     # pb2json 加密传输新协议
#     encjson = EncryptJson(GlobalVar.URL_PAY_IN)
#     result = encjson.post('/api/conf/v1/service-base-info', {'partnerId': '2031'})
#     print('客服联系方式:', result['data']['contactInfo'])
#     result = encjson.post('/api/conf/v1/package-name', {})
#     print(result['data']['walletPackageName'])

#     # grant multi voucher
#     for i in range(1):
#         tps = 4
#         ssoids = '2086100900', '2076075925', '2086628989', '2086776969'
#         case_file_path = os.path.join(CASE_SRCFILE_ROOTDIR, 'http', 'inland.xlsx')
#         vouinfo = VouInfo(case_file_path)
#         vouinfo.create()
#         all_request_ids = {}
#         all_tasks = []
#         thr_num = int(tps/len(ssoids))
#         executor = ThreadPoolExecutor(max_workers=thr_num)
#         for ssoid in ssoids:
#             httpobj = HttpGrantMultiVous(vouinfo, ssoid, '2031')
#             [all_tasks.append(executor.submit(httpobj.post))
#                               for i in range(executor._max_workers)]
#             start = time.perf_counter()
#             while time.perf_counter() - start < 10:
#                 if len(httpobj.request_ids) == executor._max_workers:
#                     break
#                 else:
#                     time.sleep(0.5)
#             else:
#                 print('实际发送请求数: %d\t期望发送请求数: %d' %(len(httpobj.request_ids), executor._max_workers))
#                 raise TimeoutError('Exceed 10s, timeout occurred!!!')
#             for reqid in httpobj.request_ids:
#                 all_request_ids.setdefault(ssoid, set()).add(reqid)
#         wait(all_tasks, return_when=ALL_COMPLETED)
#             exp_vou_count = httpobj.vouinfo_obj.count * executor._max_workers
#             for ssoid in ssoids:
#                 start = time.perf_counter()
#                 table_id = SeparateDbTable(ssoid).get_vou_table()
#                 sql = "SELECT COUNT(id) FROM oppopay_voucher.vou_info_%d WHERE ssoid='%s' AND createTime >= CURRENT_TIMESTAMP - INTERVAL 30 SECOND ORDER BY id DESC;" %(table_id, ssoid)
#                 while time.perf_counter() - start < 10:
#                     count = GlobalVar.MYSQL_IN.select_one(sql)['COUNT(id)']
#                     if count == exp_vou_count:
#                         break
#                     else:
#                         time.sleep(1)
#                 else:
#                     print('The incremental number of oppopay_voucher.vou_info_%d: %d != %d' %(table_id, count, exp_vou_count), file=sys.stderr)
#         #             raise Exception('Exceed 10s, TIMEOUT!')
#                 sql = "SELECT partnerOrder FROM oppopay_voucher.vou_info_%d WHERE ssoid='%s' AND createTime >= CURRENT_TIMESTAMP - INTERVAL 30 SECOND ORDER BY id DESC;" %(table_id, ssoid)
#                 db_request_ids = set(chain(*[d.values() for d in GlobalVar.MYSQL_IN.select(sql)]))
#                 for reqid in all_request_ids[ssoid]:
#                     with IgnoreException(None) as ign:
#                         assert reqid in db_request_ids, 'requestId %s not in oppopay_voucher.vou_info_%d' %(reqid, table_id)

#     # grant single voucher
#     tps = 1
# #     ssoids = '2086100900', '2076075925', '2086628989', '2086776969'
#     ssoids = '2076074648',
#     partner_id = '5456925'
#     all_tasks = []
#     thr_num = int(tps/len(ssoids))
#     executor = ThreadPoolExecutor(max_workers=thr_num)
#     vou_types = [1, 2, 5, 7, 8]
#     random.shuffle(vou_types)
#     for ssoid, voutype in zip(*extend_to_longest([ssoids, vou_types])):
#         httpobj = HttpGrantSingleVous(voutype, ssoid, partner_id=partner_id)
#         [all_tasks.append(executor.submit(httpobj.post))
#                           for i in range(executor._max_workers)]
#     wait(all_tasks, return_when=ALL_COMPLETED)
    
    # 签约并支付，alipay签解约回调
#     raw_resp = '{charset=UTF-8, notify_time=2021-06-26 18:03:48, alipay_user_id=2088202596648570, sign=FD8KP85KdUlAWXRw4bXx0kKUkeBo1gbSR36bjLzoPs/yie4NF/JbOdhEmZoC+0iNbWnFUo7yKu0k5D8NuF7p+iKH2UfAbcW3WuO+j6pFPdyZwFTsFlLLvw63z5iWYXH0nSaD+qbI/mai9vFA/Vv3xbDFbyU/uqdNg4+7cqZ7N5KCMwMg3APjGJRKb3SOfZXUYHSe+QaBVDKPj/CY5lJr1F1Lub/M/b/nbAi2+84dr6OxKlcCOo6QIgCnM1j3lIPAH0fNI9LKmhnUfQJqO1UNPI6MtTWQgppQPzuPM4PjuZyBlOCUBBlzAbWojZNVE1RgTtxAcZIWNyE8G1iB9QA/Tw==, external_agreement_no=SN202106261803291250166665280727, version=1.0, sign_time=2021-06-26 18:03:47, notify_id=2021062600222180348058541442634678, notify_type=dut_user_sign, agreement_no=20215426731249915557, auth_app_id=2016120904060189, invalid_time=2115-02-01 00:00:00, personal_product_code=GENERAL_WITHHOLDING_P, valid_time=2021-06-26 18:03:47, app_id=2016120904060189, sign_type=RSA2, alipay_logon_id=280***@qq.com, status=NORMAL, sign_scene=INDUSTRY|GAME_CHARGE}'
#     ali_sign_scarlet_by_raw_resp(raw_resp)

    signpay = AutoRenewDebug('2086776969', '2031')
    # 解约
#     signpay.un_sign('20215426731000052557', '7d40f413cebf4fa7bf729803eb579662', 'alipay')   #支付宝
#     signpay.un_sign('2017957262', '0CDOsHN5EGqLSBK1og2j7laZu3Qvmi9T', 'wxpay')   #微信
    # 微信解约回调
    raw_xml = ''
    signpay.wx_unsign(raw_xml)
    # 自动扣费
#     signpay.auto_renew_out(agreement_no='2017957262', pay_type='wxpay', third_part_id='0s4ns6EZ8ym0kW_JzUeps')
#     signpay.auto_renew_out(agreement_no='20215426731000052557', pay_type='alipay', third_part_id='2088202596648570', amount=0.01)
    # 签约并支付下单接口
#     signpay = AutoRenew('wxpay', '2031', '280', '280')
#     signpay.auto_renew(1)

#     # 新支付中心单接口调试
#     paycenter_dubbo = PayCenterDubbo(partner_code='2031')
#     paycenter_dubbo.create_direct_pay('wxpay', 0.01, 0.01)

#     get_available_voucher_by_type('2086776969', '消费折扣')
