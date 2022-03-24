# coding=utf-8
env_id = 'product'
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
from lib.common.utils.globals import GlobalVar, CASE_SRCFILE_ROOTDIR, HTTPJSON_SCARLET, redis
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
from lib.common_biz.oppo_cloud import HttpOPPOCloud
from lib.common_biz.user_account import Account
from lib.common_biz.ocloud import Ocloud
from lib.common.algorithm.sha_256 import sha_256
from lib.common_biz.sign import Sign
from lib.common_biz.find_key import GetKey


if __name__ == '__main__':
    # Redis操作
    #     print(redis.get('pay_biz_paycenter:credit_day_limit:20210824:2086776969'))
    #     Nearme().query_balance('2086776969')    #pay_cocoin_3.pay_user_info_158
    flag_coin = "0"
    if flag_coin == "1":
        # 发
        # Nearme().nearme_add_subtract("10000", "2000060346", 0)
        Nearme(in_out='oversea').nearme_add_subtract_oversea("10000", "2000060346", 'SG', 0)
        Nearme().query_balance('2000060346')
    if flag_coin == "2":
        # 扣
        Nearme().nearme_add_subtract("0.01", "2000060346", 1)
        Nearme().query_balance('2000060346')
    #     ssoid = '2086788561'    #黄勇翔
    #     ssoid = '2076074648' '2086780063'   #黄小静
    #     ssoid = '2076079836'    #陈华平
    #     ssoid = '2086631885'    #彭哲
    #     ssoid = '2076064003'    #江厚军
    #     ssoid = '2000060346'    # 周正攀
    partner_id = '9809089'    #游戏 5456925, 主题 9809089
    ssoid = '2086776969'
    if env_id.isdigit():
        voucher = Voucher()
        for flag in range(1, 1):
            if flag == 1:
                # 满减(抵扣)
                voucher.grant_check_voucher(partner_id, "KB_COUPON", "DIKOU", "10", "8.99", ssoid)
            if flag == 2:
                # 消费
                for _ in range(random.choice(range(1, 11))):
                    voucher.grant_check_voucher(partner_id, "KB_COUPON", "XIAOFEI", "0", "1", ssoid)
            if flag == 3:
                # 折扣
                voucher.grant_check_voucher(partner_id, "KB_COUPON", "DAZHE", "2", "0", ssoid, ratio=0.68, maxCutAmount='1')
            #                 voucher.grant_check_voucher(partner_id, "KB_COUPON", "DAZHE", "1", "0", ssoid, ratio=0.1, maxCutAmount='1')
            if flag == 4:
                # 消费折扣
                voucher.grant_check_voucher(partner_id, "KB_COUPON", "XIAOFEI_DAZHE", "5", "0", ssoid, ratio=0.01, maxCutAmount='10')
            if flag == 5:
                # 红包券
                for _ in range(random.choice(range(1, 11))):
                    voucher.grant_check_voucher(partner_id, "KB_COUPON", "RED_PACKET_COUPON", "0", "10", ssoid)
            if flag == 6:
                # 海外满减
                Voucher("oversea").grant_check_voucher("9809089", "KB_COUPON", "DIKOU", "10000", "7500", ssoid, "ID", "IDR")

    #                 Voucher("oversea").grant_check_voucher("9809089", "KB_COUPON", "DAZHE", "10000", "0", ssoid, "ID", "IDR", ratio=0.1, maxCutAmount='10000')
    #                 Voucher("oversea").grant_check_voucher('9809089', "KB_COUPON", "XIAOFEI_DAZHE", "10000", "0", ssoid, "ID", "IDR", ratio=0.2, maxCutAmount='10000')
    #                 Voucher("oversea").grant_check_voucher("980908902", "KB_COUPON", "DIKOU", "10000", "7500", ssoid, "ID", "IDR")
    #                 Voucher("oversea").grant_check_voucher("980908902", "KB_COUPON", "DAZHE", "10000", "0", ssoid, "ID", "IDR", ratio=0.1, maxCutAmount='10000')
    #                 Voucher("oversea").grant_check_voucher('980908902', "KB_COUPON", "XIAOFEI_DAZHE", "10000", "0", ssoid, "ID", "IDR", ratio=0.2, maxCutAmount='10000')
    # 通过批次号审核券
    #     VoucherInland().checkVoucher('a39a8a029ebc4055bdc9a489d9a765d5')

    # 查询优惠券
    #     Voucher().query_voucher_by_id('2086776969', '62641621')
    #     Voucher().query_all_useable('2086776969', partner_id='2031')

    # http自动退款
    session = None
    if env_id == 'grey':
        session = HttpJsonSession('https://pre-nativepay.keke.cn')  # 灰度域名
    elif env_id == 'product':
        session = HttpJsonSession('https://nativepay.keke.cn')  # 正式域名
    refund = Refund('2086797854', http_session=session or GlobalVar.HTTPJSON_IN)   # 14213467928
    # 根据业务订单号退款
    per_amount = 1
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
    # refund.refund_by_ssoid_in_timerange(start_time='2021-12-22 00:00:00', ssoid='2076064003')

    # 审批退款：order审批，dispatcher退款
    # refund = GrantRefund("2086776969")
    # refund.refund_by_pay_req_id('', 0.01)
    #     refund.refund_by_amount('', amount=0.01)
    #     refund.refund_by_partner_order('')
    #     refund.refund_by_ssoid()
    #     refund.refund_by_partner_code_in_timerange('247628518', start_time='2021-07-01 00:00:00')
    #     refund.refund_by_ssoid_in_timerange(start_time='2021-07-01 00:00:00')

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
    # for i in range(1):
    #     tps = 4
    #     ssoids = '2086100900', '2076075925', '2086628989', '2086776969'
    #     case_file_path = os.path.join(CASE_SRCFILE_ROOTDIR, 'http', 'inland.xlsx')
    #     vouinfo = VouInfo(case_file_path)
    #     vouinfo.create()
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
#
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

    # 签约并支付，alipay签/解约回调 newAlipaySignNotify get input:
    raw_resp = '{charset=UTF-8, notify_time=2022-02-15 18:31:49, alipay_user_id=2088622606365602, sign=wbBfgwrWuebBVC+Rm2WAZfsdpCSiG35cV5aMb8o5Lwnr1kSRWjXH2R2PzFW6zNvuRdzyz6rYE4SOAi/jLRvh02mGt7FZgljrOnsVOG+ByWgRRE2b9AQUTOAI1ICoPBzFFBmR1DA4ys4nj8eWMjVKn1F1hqUBpFP4uf82LJBMnkXETfQIbmMb2qMlaMa+aSIZu25/Kc2ORVHcpBefy5BKH4zZ9AhxJnUaWBDmiqFevyaTzkTKo6L+PB0tp86mhak4RpWeiMxgaGtXrwptzA0WmP1/pqA/k52plPXPUbDk/rCgOiknwhD2WOJo+cUZdsDpkXCSt61pVero88nLIHM2Jw==, external_agreement_no=SN202202151831387827725836406722, version=1.0, sign_time=2022-02-15 18:31:49, notify_id=2022021500222183149041681455748210, notify_type=dut_user_sign, agreement_no=20225015810059007660, auth_app_id=2016120904060189, invalid_time=2115-02-01 00:00:00, personal_product_code=GENERAL_WITHHOLDING_P, valid_time=2022-02-15 18:31:49, app_id=2016120904060189, sign_type=RSA2, alipay_logon_id=hua***@163.com, status=NORMAL, sign_scene=INDUSTRY|GAME_CHARGE}'
    # ali_sign_scarlet_by_raw_resp(raw_resp)

    signpay = AutoRenewDebug('2086776969', '247628518', '2476285180010')
    # signpay = AutoRenewDebug('2086776969', '72724314', '727243140015')
    # signpay = AutoRenewDebug('2086776969', '72727676', '334084867195408384')
    # signpay = AutoRenewDebug('2086776969', '2031', '20310001')
    # 业务方发起解约
    # signpay.un_sign('20216006774774573557', 'alipay')   #支付宝
    # signpay.un_sign('202112065890302970', 'wxpay')   #微信
    # signpay.newtv_unsign('3wdMysDt4NUj61ubT2vhlpSocnPY7kCq')   #newtv解约 /gateway/sign/cancel
    # 微信解约回调 /opaycenter/wxpaysignnotify <change_type>ADD</change_type>
    raw_xml = '<xml><change_type>DELETE</change_type><contract_code>5ba44adcb6ad35e3840b8965f358b8af</contract_code><contract_id>202112225344271383</contract_id><contract_termination_mode>3</contract_termination_mode><mch_id>1502416961</mch_id><openid>oxad21FZpQ-KWu3ARiRZVcke72AM</openid><operate_time>2021-12-22 20:23:42</operate_time><plan_id>130461</plan_id><request_serial>164017574651946304</request_serial><result_code>SUCCESS</result_code><return_code>SUCCESS</return_code><return_msg>OK</return_msg><sign>0332CFF3B5CCBB4E0F9BFD50F6FC8D2D</sign></xml>'
    # signpay.wx_unsign(raw_xml)

    # 自动扣费
    # signpay.auto_renew_out(agreement_no='202108205923224378', pay_type='wxpay', third_part_id='oCg6Xt-0s4ns6EZ8ym0kW_JzUeps')
    # signpay.auto_renew_out(agreement_no='20215426731000052557', pay_type='alipay', third_part_id='2088202596648570', amount=0.01)

    # 签约并支付下单接口
    #     signpay = AutoRenew('wxpay', '2031', '280', '280')
    #     signpay.auto_renew(1)

    #     # 新支付中心单接口调试
    #     paycenter_dubbo = PayCenterDubbo(partner_code='2031')
    #     paycenter_dubbo.create_direct_pay('wxpay', 0.01, 0.01)

    #     get_available_voucher_by_type('2086776969', '消费折扣')

    # 云平台查询SLA接口
    #     oppo_cloud = HttpOPPOCloud()
    #     print(oppo_cloud.get_sla_interface('fspay', is_dash=True))

    # 查询验证码
    # account = Account()
    # account.login()
    # print(account.get_verification_code('14213467928', 'http://auto.uc.oppoer.me'))
    # print(account.get_verification_code('14441120298'))

    # 云服务接口
    ocloud = Ocloud()
    # ocloud.update_expire_time()
    
    # newTV
    req = {
        "aheadOfTime": "86400",
        "amount": 999,
        "contractNotifyUrl": "http://pay.pay-test.wanyol.com/sign-result-test",
        "countryCode": "CN",
        "currency": "CNY",
        "interval": "31",
        "intervalType": "2",
        "nextAmount": "1",
        "notifyUrl": "http://pay.pay-test.wanyol.com/pay-result-test",
        "orderName": "连续包月",
        "papayType": "2",
        "partnerId": "72727676",
        "partnerOrder": create_random_str(32),
        "payType": "newtv",
        "planId": "122222",
        "productId": "334084867195408384",
        "sign": '',
        "userId": "2086776969"
    }
    # private_key = GetKey('72727676').get_key_from_merchant()
    # req['sign'] = sha_256(Sign(req).join_asc_have_key("&key=") + private_key)
    # GlobalVar.HTTPJSON_GW_IN.post('/gateway/wxpay/qrcode/signAndPay', data=req)
