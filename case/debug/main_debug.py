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
from lib.common.utils.misc_utils import create_random_str
from lib.common_biz.find_database_table import SeparateDbTable
from lib.interface_biz.dubbo.near_me import Nearme
from lib.interface_biz.dubbo.vou import Voucher
from lib.common.session.http.http_json import EncryptJson, HttpJsonSession
from lib.common.utils.globals import GlobalVar, CASE_SRCFILE_ROOTDIR
from lib.interface_biz.http.refund import Refund
from lib.common.algorithm.aes import AES4J
from lib.common.exception.intf_exception import IgnoreException
from lib.interface_biz.http.grant_voucher import HttpGrantMultiVous, VouInfo
from lib.common.exception import WaitUntilTimeOut


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

#     # http自动退款
#     session = None
#     if env_id == 'grey':
#         session = HttpJsonSession('https://pre-nativepay.keke.cn')  # 灰度域名
#     elif env_id == 'product':
#         session = HttpJsonSession('https://nativepay.keke.cn')  # 正式域名
#     refund = Refund('2086100900', http_session=session or GlobalVar.HTTPJSON_IN)   # 14213467928
#     per_amount = 0.01
#     total_amount = 0.01
#     loop_num = int(total_amount/per_amount)
#     for i in range(loop_num): 
#         while True:
#             response = refund.httpjson_refund('', '5456925', per_amount, pay_req_id='')
#             if response['resMsg'] == '退款失败':
#                 time.sleep(1)
#             else:
#                 break

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

    # grant multi voucher
    case_file_path = os.path.join(CASE_SRCFILE_ROOTDIR, 'http', 'inland.xlsx')
    vouinfo = VouInfo(case_file_path)
    vouinfo.create()
    ssoids = '2086100900', '2076075925', '2086628989'
    all_request_ids = {}
    all_tasks = []
    thr_num = int(1000/len(ssoids))
    executor = ThreadPoolExecutor(max_workers=thr_num)
    for ssoid in ssoids:
        httpobj = HttpGrantMultiVous(vouinfo, ssoid, '2031')
        [all_tasks.append(executor.submit(httpobj.post))
                          for i in range(executor._max_workers)]
        with WaitUntilTimeOut(len(httpobj.request_ids) == executor._max_workers, interval=0.5) as wt:
            try:
                wt.wait()
            except:
                print('实际发送请求数: %d\t期望发送请求数: %d' %(len(httpobj.request_ids), executor._max_workers))
                raise
        for reqid in httpobj.request_ids:
            all_request_ids.setdefault(ssoid, set()).add(reqid)
    wait(all_tasks, return_when=ALL_COMPLETED)
    exp_vou_count = httpobj.vouinfo_obj.count * executor._max_workers
    for ssoid in ssoids:
        start = time.perf_counter()
        table_id = SeparateDbTable(ssoid).get_vou_table()
        sql = "SELECT COUNT(id) FROM oppopay_voucher.vou_info_%d WHERE ssoid='%s' AND createTime >= CURRENT_TIMESTAMP - INTERVAL 30 SECOND ORDER BY id DESC;" %(table_id, ssoid)
        while time.perf_counter() - start < 10:
            count = GlobalVar.MYSQL_IN.select_one(sql)['COUNT(id)']
            if count == exp_vou_count:            
                break
            else:
                time.sleep(1)                
        else:
            print('The incremental number of oppopay_voucher.vou_info_%d: %d != %d' %(table_id, count, exp_vou_count), file=sys.stderr)
            raise Exception('Exceed 10s, TIMEOUT!')
        sql = "SELECT partnerOrder FROM oppopay_voucher.vou_info_%d WHERE ssoid='%s' AND createTime >= CURRENT_TIMESTAMP - INTERVAL 30 SECOND ORDER BY id DESC;" %(table_id, ssoid)
        db_request_ids = set(chain(*(d['partnerOrder'] for d in GlobalVar.MYSQL_IN.select(sql))))
        for reqid in all_request_ids[ssoid]:
            with IgnoreException(None) as ign:
                assert reqid in db_request_ids, 'requestId %s not in oppopay_voucher.vou_info_%d' %(reqid, table_id)
    
        
