#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 22:55
# comment: 接口参数替换
import time
from lib.common.algorithm.cipher import Cipher
from lib.common.algorithm.md5 import md5
from lib.common.algorithm.rsa import rsa
from lib.common.file_operation.config_operation import Config
from lib.common.utils.globals import GlobalVar
from lib.common_biz.find_key import GetKey, is_get_key_from_db
from lib.interface_biz.http.pay_pass import Pass, pass_no_login_in, get_process_token
from lib.common.utils.meta import WithLogger
from lib.common_biz.file_path import do_case_path, key_path
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import expend_pay_sign_string, oversea_header_sign_string, simple_pay_sign_string, Sign


def get_tp_rv(pay_method):
    """
    :return:
    """
    t_p = ""
    r_v = ""
    m_p = ""
    if pay_method == "recharge":
        pass_params = Pass().pass_recharge()
        r_v = pass_params[0]
        t_p = pass_params[1]
        m_p = pass_params[2]
    elif pay_method in ("expend", 'recharge_spend'):
        pass_params = Pass().pass_recharge_spend()
        r_v = pass_params[0]
        t_p = pass_params[1]
        m_p = pass_params[2]
    elif pay_method == "direct":
        pass_params = Pass().pass_direct_pay()
        r_v = pass_params[0]
        t_p = pass_params[1]
        m_p = pass_params[2]
    elif pay_method == "no_login":
        pass_params = pass_no_login_in()
        r_v = pass_params[0]
        t_p = pass_params[1]
        m_p = pass_params[2]
    return r_v, t_p, m_p


class ReplaceParams(metaclass=WithLogger):
    def __init__(self, case):
        self.case = self.req = case

    def replace_native(self, pay_method, voucher_info=None):
        partner_order = RandomOrder(32).random_string()
        tp_rv = get_tp_rv(pay_method)
        r_v = tp_rv[0]
        t_p = tp_rv[1]
        m_p = tp_rv[2]
        if self.case['header']['sdkVer'] == '':
            self.case['header']['sdkVer'] = int(Config(do_case_path).read_config("sdk_ver", 'version'))
        if 'basepay' in self.case:
            if self.case['basepay']['partnerorder'] == '':
                self.case['basepay']['partnerorder'] = partner_order
        # 部分接口partnerOrder未包在basepay中
        if 'partnerOrder' in self.case:
            self.case['partnerOrder'] = partner_order
        # 部分接口含有order
        if 'order' in self.case:
            self.case['order'] = partner_order
        if 'expendRequest' in self.case:
            if self.case['header']['t_p'] == '' and self.case['header']['r_v'] == '':
                self.case['header']['t_p'] = t_p
                self.case['header']['r_v'] = r_v
            # 若expendpay,对若expendpay header中的t_p和r_v进行替换
            if self.case['expendRequest']['header']['t_p'] == '' and self.case['expendRequest']['header']['r_v'] == '':
                self.case['expendRequest']['header']['t_p'] = t_p
                self.case['expendRequest']['header']['r_v'] = r_v
            # 替换partnerOrder（用例中需要的替换该字段为空 ""）
            if self.case['expendRequest']['partnerOrder'] == '':
                self.case['expendRequest']['partnerOrder'] = partner_order
            # 替换优惠券
            if 'voucherId' in self.case['expendRequest']:
                self.case['expendRequest']['voucherId'] = voucher_info["id"]
                self.case['expendRequest']['voucherType'] = voucher_info["type"]
                self.case['expendRequest']['voucherCount'] = voucher_info["count"]
            # 替换expendpay中的sign
            if self.case['expendRequest']['sign'] == '':
                sign_string = expend_pay_sign_string(GlobalVar.TOKEN,
                                                     self.case['header']['package'],
                                                     self.case['expendRequest']['partnerid'],
                                                     self.case['expendRequest']['partnerOrder'],
                                                     self.case['expendRequest']['productname'],
                                                     self.case['expendRequest']['productdesc'],
                                                     self.case['expendRequest']['price'],
                                                     self.case['expendRequest']['count'])
                # 私钥无法拿到，只拿到测试业务线的秘钥，存放在配置文件中
                key = Config(key_path).read_config("expend_pay", "key_2031")
                self.case['expendRequest']['sign'] = rsa(sign_string, key)
        if 'expendRequest' not in self.case:
            if self.case['header']['t_p'] == '' and self.case['header']['r_v'] == '':
                self.case['header']['t_p'] = t_p
                self.case['header']['r_v'] = r_v
        # 最外层sign 疑似未校验
        if 'sign' in self.case:
            # common_sign_string = Sign(self.case).pb_common_sign_string(m_p)
            # self.case['sign'] = md5(common_sign_string)
            sign_string = simple_pay_sign_string(self.case['header']['package'], self.case['basepay']['partnercode'],
                                                 self.case['basepay']['partnerorder'], self.case['amount'], self.case['type'])
            self.case['sign'] = Cipher(sign_string).cipher()
        return self.case

    def replace_standard(self, pay_method):
        """
            basehead out 头部token 以及 r_v替换
            :param pay_method:
            :return:
            """
        r_v = get_tp_rv(pay_method)[0]
        # self.case['header']['version'] = Config(do_case_path).read_config("sdk_ver", "version")
        if self.case ['header']['appVerison'] == '':
            self.case['header']['appVerison'] = Config(do_case_path).read_config("apk_ver_oversea", "version")
        if self.case['header']['token'] == '':
            self.case['header']['token'] = GlobalVar.TOKEN
        if self.case['header']['token'] == 'no_login':
            self.case['header']['token'] = ''
        if self.case['header']['r_v'] == '':
            self.case['header']['r_v'] = r_v
        if 'partnerOrder' in self.case:
            if self.case['partnerOrder'] == '':
                self.case['partnerOrder'] = RandomOrder(32).random_string()
        if self.case['header']['sign'] == '':
            self.case['header']['sign'] = md5(oversea_header_sign_string(
                                                        self.case['header']['version'],
                                                        self.case['header']['token'],
                                                        self.case['header']['model'], self.case['header']['apntype'],
                                                        self.case['header']['package'], self.case['header']['r_v'],
                                                        self.case['header']['sdkVer'],
                                                        self.case['header']['appVerison']))


def replace_gateway(case_req, app_id):
    """
    gateway接口常见参数替换方法
    :return:
    """
    key = ''
    if is_get_key_from_db():
        key = GetKey(app_id).get_key_from_server_info()
    else:
        key = Config(key_path).as_dict('gateway_app_id')["key_" + app_id]
    case_req['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
    case_req['service'] = case_req['service']
    # bizContent 传输方式为字符串类型
    case_req['bizContent'] = str(case_req['bizContent'])
    # 签名替换
    if case_req['sign'] == '':
        sign_string = Sign(case_req).join_asc_have_key() + key
        case_req['sign'] = md5(sign_string)


def replace_http_json(req):
    """
    新版本客户端参数替换
    :return:
    """
    if req['processToken'] == "":
        req['processToken'] = get_process_token()
    return req