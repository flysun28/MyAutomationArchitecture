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
from case.debug.inland.json.auto_renew import AutoRenew
from lib.common_biz.fiz_assert import is_assert, ASSERTION_IN
from lib.common_biz.choose_scarlett import choose_scarlett
from lib.interface_biz.http.query_result import queryResult
from lib.interface_biz.dubbo.refactor.paycenter import PayCenterDubbo

if __name__ == '__main__':
    flag_coin = "0"
    if flag_coin == "1":
        # 发
        Nearme().nearme_add_subtract("0.01", "2086776969", 0)
    if flag_coin == "2":
        # 扣
        Nearme().nearme_add_subtract("0.01", "2086776969", 1)
    flag = "0"
    if flag == "1":
        # 满减
        vou_info = Voucher().grantVoucher("5456925", "KB_COUPON", "DIKOU", "1", "0.99", "2086776969")
        Voucher().checkVoucher(vou_info['batchId'])
        # 消费
    if flag == "2":
        vou_info = Voucher().grantVoucher("2031", "KB_COUPON", "XIAOFEI", "0", "0.01", "2086776969")
        Voucher().checkVoucher(vou_info['batchId'])
    if flag == "3":
        # 红包券
        vou_info = Voucher().grantVoucher("5456925", "KB_COUPON", "RED_PACKET_COUPON", "0", "10", "2086776969")
        Voucher().checkVoucher(vou_info['batchId'])
    if flag == "4":
        # 海外满减
        vou_info = Voucher("oversea").grantVoucher("9809089", "KB_COUPON", "DIKOU", "10000", "7500", "2076075925", "VN",
                                                   "VND")
        Voucher("oversea").checkVoucher(vou_info['batchId'])
    # 查询优惠券
#     Voucher().query_voucher('2086776969', '62641621')

#     # 审批退款
#     refund = GrantRefund("2086776969")
#     refund.refund_by_pay_req_id('KB202105021143102086776969517632')
    
    # http自动退款
    session = None
    if env_id == 'grey':
        session = HttpJsonSession('https://pre-nativepay.keke.cn')  # 灰度域名
    elif env_id == 'product':
        session = HttpJsonSession('https://nativepay.keke.cn')  # 正式域名
    refund = Refund('2086776969', http_session=session or GlobalVar.HTTPJSON_IN)   # 14213467928
#     # 根据业务订单号退款
#     per_amount = 0
#     total_amount = 0
#     loop_num = int(total_amount/per_amount)
#     for i in range(loop_num): 
#         while True:
#             response = refund.httpjson_refund('', '5456925', per_amount, pay_req_id='')
#             if response['resMsg'] == '退款失败':
#                 time.sleep(1)
#             else:
#                 break
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
#     ssoids = '692039187',
#     all_tasks = []
#     thr_num = int(tps/len(ssoids))
#     executor = ThreadPoolExecutor(max_workers=thr_num)
#     vou_types = [1, 2, 5, 7, 8]
#     random.shuffle(vou_types)
#     for ssoid, voutype in zip(*extend_to_longest([ssoids, vou_types])):
#         httpobj = HttpGrantSingleVous(voutype, ssoid, partner_id='5456925')
#         [all_tasks.append(executor.submit(httpobj.post))
#                           for i in range(executor._max_workers)]
#     wait(all_tasks, return_when=ALL_COMPLETED)
    
    # 签约并支付
#     pay_channel = ''
#     if pay_channel == 'ali':
#         raw_resp = '{charset=UTF-8, notify_time=2021-04-27 18:02:26, alipay_user_id=2088202596648570, sign=lNpmgEGYtr1qMYFr2WDwP+sgaSt+tLdtMYwBDTwtQTomtkS1tL9DGDSxrdPfxdfWluWGikCVzVvf3PMIvVU+6vcn0SO1rxLIzkxtflJFa5YBZzC1yF++CJkwGaVZq6j/nh7FrSvpX4DMfOD5txd1PCZKkJmBr6rIMv6BISGsfqHwcZC4WYgqPx9ky0wfjuCyybGzqHrCkPX3syOyzGX13vpLUxMViV6SCwZKKCVD4BV9Kp0zeBQ//UVlshupzOfwdLCN9zw9NIVKm/LqCGp1Hb0+o7Vg7saf5fZ5A1UgRK/AfQhtjI+WSOufsvByrRgSEu+u0+jSF5dVrr0+HUh76w==, external_agreement_no=SN202104271802133716021610682168, version=1.0, sign_time=2021-04-27 18:02:26, notify_id=2021042700222180226038661428420836, notify_type=dut_user_sign, agreement_no=20215227712921458557, auth_app_id=2016120904060189, invalid_time=2115-02-01 00:00:00, personal_product_code=GENERAL_WITHHOLDING_P, valid_time=2021-04-27 18:02:26, app_id=2016120904060189, sign_type=RSA2, alipay_logon_id=280***@qq.com, status=NORMAL, sign_scene=INDUSTRY|GAME_CHARGE}'
#         ali_sign_scarlet_by_raw_resp(raw_resp)
#     elif pay_channel == 'wx':
#         raw_xml = ''
#         requests.post(HTTPJSON_SCARLET.prefix + "/opaycenter/wxpaysignnotify", raw_xml)    
#     signpay = AutoRenew('2086776969', '2031')
    # 解约
#     signpay.un_sign('20215302714334851557', 'c7bf8b413ef94834a7e1b65b4106f49e', 'alipay')
#     # 微信解约回调
#     raw_xml = '<xml><change_type>DELETE</change_type><contract_code>SN202105021509574048153102744280</contract_code><contract_id>202105025876133076</contract_id><contract_termination_mode>2</contract_termination_mode><mch_id>1259634601</mch_id><openid>oCg6Xt7eyxUA67wAAKdXgC3l3WG0</openid><operate_time>2021-05-02 15:12:28</operate_time><plan_id>131584</plan_id><request_serial>161993939740840877</request_serial><result_code>SUCCESS</result_code><return_code>SUCCESS</return_code><return_msg>OK</return_msg><sign>E334A61BF3588E8BE161E47EBD474562</sign></xml>'
#     resp = requests.post(HTTPJSON_SCARLET.prefix + "/opaycenter/wxpaysignnotify", raw_xml)
#     print(resp.content)
    # 自动扣费
#     signpay.auto_renew_out(agreement_no='202105025876133076', pay_type='wxpay')

#     # 新支付中心单接口调试
#     paycenter_dubbo = PayCenterDubbo(partner_code='2031')
#     paycenter_dubbo.create_direct_pay('wxpay', 0.01, 0.01)
