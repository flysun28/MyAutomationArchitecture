'''
Created on 2021年2月26日
@author: 80319739
'''
import time
import random
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.env import get_dubbo_info, set_global_env_id
from lib.common_biz.order_random import RandomOrder
from lib.common.utils.globals import GlobalVar
from lib.common_biz.choose_scarlett import choose_scarlett
from lib.interface_biz.http.query_result import queryResult
from lib.common_biz.fiz_assert import is_assert, ASSERTION_IN


class PayCenterDubbo():

    def __init__(self, partner_code='2031'):
        self.ssoid = GlobalVar.SSOID
        self.partner_code = partner_code
        self.partner_order = None
        self.channel_type = "NATIVE"
        self.trade_type = "PAY"
        self.req = None
        dubbo_info = get_dubbo_info("pay_biz_paycenter")
        self.conn = DubRunner(*dubbo_info)
    
    def create_payorder(self, original_amount, amount, channel='', kebi_spent=0, voucher_info={}, ssoid='', **kwargs):
        '''
        |       参数名      | 限制 |      类型     |      取值范围      |   说明   |
        | partnerOrder     | 必填 |    Integer    |                  | 业务订单号 |
        | partnerCode      | 必填 |    String     |                  | 业务线ID |
        | originalAmount   | 必填 |    BigDecimal |                  | 商品原价(单位元) =amount+kebiSpent+voucherAmount    
        | amount           | 选填 |    BigDecimal |                  | 渠道支付金额，amount, kebiSpent, voucherAmount 不能同时为空    
        | productsName     | 必填 |    String     |                  | 商品名称        
        | counts           | 选填 |               |                  | 商品数量        
        | ssoid            | 选填 |    String     |   
        | channnelType     | 选填 |    String     |  
        | payType          | 选填 |    String     | wxpay,alipay,alipay_hb,szfpay,qqwallet | 支付方式，amount不为空时，必填。例如：alipay,wxpay |   
        | directPay        | 选填 |    String     |                  | ZHICHONG 的话, payReqId开头字母为KB, 其余的话, 均为RM |
        | presentAmount    | 选填 |    String     |                  | amount, kebiSpent, voucherAmount不能同时为空 |
        | countryCode      | 选填 |    timestamp  |      
        | currency         | 选填 |    timestamp  |  
        | kebiSpent        | 选填 |    Long       |                  | 可币支付金额，amount, kebiSpent, voucherAmount不能同时为空 |
        | voucherAmount    | 选填 |    BigDecimal |                  | 优惠券金额，voucherAmount 和 voucherInfo 需同时共存 |
        | voucherInfo      | 选填 |    String     |                  | 优惠券信息JSON串 |
        | voucherId        | 选填 |    String     |                  |
        | tradeType        | 选填 |    String     | KB, ZHICHONG     | 仅用于生成兼容的PayReqID, ZHICHONG 的话, payReqId开头字母为KB, 其余的话, 均为RM |
        | contents         | 选填 |    String     |                  | 商品介绍 |
        | mobileNum        | 选填 |    String     |
        | imei             | 选填 |    String     |   
        | imsi             | 选填 |    String     |   
        | ip               | 选填 |    String     |   
        | mac              | 选填 |    String     |  
        | model            | 选填 |    String     |   
        | appPackage       | 选填 |    String     |   
        | appVer           | 选填 |    String     |   
        | sdkVer           | 选填 |    String     | 
        | channelId        | 选填 |    String     |   
        | gameType         | 选填 |    String     |   
        | extra            | 选填 |    String     |   
        | remark           | 选填 |    String     |   
        | discountInfo     | 选填 |    String     |   
        | openid           | 选填 |    String     |   
        | brandType        | 选填 |    String     |   
        | mobileOsVer      | 选填 |    String     |   
        | platform         | 选填 |    String     |   
        | screenInfo       | 选填 |    String     |   
        | factor           | 选填 |    String     |           | 使用优惠券时必填 |
        | notifyUrl        | 选填 |    String     |   
        | subPartnerOrders | 选填 |  List<String> |           | 合单的子订单号列表 |
        | payContext       | 选填 |  Map<String,Object> |     | 渠道相关数据，amount不为空时，必填。例如: SZF需要cardAmount,cardNo,cardPwd |
        '''
#         table = pandas.read_html('https://doc.myoas.com/display/pingtai/pay-biz-paycenter+PayService', encoding='utf-8')[0]
#         print(table)
        if ssoid:
            self.ssoid = ssoid
        is_direct_pay = kwargs.get('directPay') or kwargs.get('direct_pay')        
        if not is_direct_pay:
            is_direct_pay = "ZHICHONG" if amount and kebi_spent == 0 and voucher_info == {} else 'KB'
        self.req = {
            'partnerOrder': '',
            'partnerCode': self.partner_code,
            'originalAmount': original_amount,
            'amount': amount,
            'productsName': 'SecurityPayments test',
            'counts': '1',
            'ssoid': self.ssoid, 
            'channelType': self.channel_type,
            'payType': channel, 
            'directPay': is_direct_pay,
            'presentAmount': 0, 
            'countryCode': 'CN', 
            'currency': 'CNY',
            'kebiSpent': kebi_spent,
            'voucherAmount': 0, 'voucherInfo': '', 'voucherId': '', 
            'tradeType': self.trade_type, 
            'contents': '', 'mobileNum': '', 'imei': '', 'imsi': '', 'ip': '', 'mac': '', 'model': '', 
            'appPackage': 'com.example.pay_demo',
            'appVer': '265', 'sdkVer': '1.0', 'channelId': '', 'gameType': '',
            'extra': '', 'remark': '', 'discountInfo': '',
            'openid': '', 'brandType': 'OPPO', 'mobileOsVer': '', 'platform': '',
            'screenInfo': '', 'factor': '', 'notifyUrl': '', 'subPartnerOrders': [],
            # SZF的话, 需要cardAmount,cardNo,cardPwd
            # alipay: 1)plugintype, 取值有 0(其他如WAP), 1(APP支付)  
            # wxpay: 1)plugintype, 取值有 0, NATIVE, JSAPI, APP 2)authorizationCode payWay是JSAPI时必填
            "payContext": {}
        }
        self.req['partnerOrder'] = kwargs.get('partner_order', RandomOrder(32).random_string())
        self.update_voucher(voucher_info)
        self.update_payContext(channel)
        if channel == 'wxpay':
            self.req['ip'] = '.'.join(map(str, random.sample(range(255), 4)))
        self.req.update(kwargs)
        return self.conn.invoke('PayService', 'tryPay', self.req, flag='JSON')

    def refund_order(self, pay_req_id, channel_refund, kebi_refund="", voucher_refund="", **kwargs):
        '''
        |    参数名      |    限制 |      类型     |  取值范围  |   说明   |
        | refundId      |    选填 |    Integer    |          | 退款ID, 做幂等判断 |
        | payReqId      |    必填 |    String     |          | 业务线ID         |
        | refund        |    选填 |    BigDecimal |          | 渠道退款金额(单位元) |
        | kebiRefund    |    选填 |    Long       |          | 可币退款金额      |
        | voucherRefund |    选填 |    String     |    Y N   | 优惠券退款标识    |
        | refundType    |    选填 |    String     |          | 退款类型         |
        | ext1          |    选填 |    String     |
        | ext2          |    选填 |    String     |
        | remark        |    选填 |    String     |
        | applyAccount  |    选填 |    String     |
        | refuseReason  |    选填 |    String     |
        | auditStatus   |    选填 |    String     |
        | approvalTime  |   选填  | LocalDateTime |
        | financeStatus |    选填 |    Boolean    |
        | batchNo       |    选填 |    BigDecimal |
        | refundReason  |    选填 |    String     |
        | fileUrl       |    选填 |    String     |
        | notifyUrl     |    选填 |    String     |
        | refundContext |    选填 | Map<String,Object> |    | 退款上下文数据, 一般存放渠道特定的参数 |
        '''
        self.req = {
            'refundId': RandomOrder(32).random_num(),
            'payReqId': pay_req_id,
            'refund': channel_refund,
            'kebiRefund': kebi_refund,
            'voucherRefund': voucher_refund,
            'refundType': '',
            'ext1': '',
            'ext2': '',
            'applyAccount': '',
            'refuseReason': '',
            'auditStatus': '',
            'approvalTime': '',
            'financeStatus': '',
            'batchNo': '',
            'refundReason': '',
            'fileUrl': '',
            'notifyUrl': '',
            'refundContext': ''
        }
        if self.req['kebiRefund'] == '':
            del self.req['kebiRefund']
        if self.req['voucherRefund'] == '':
            del self.req['voucherRefund']
        self.req.update(kwargs)
        self.conn.invoke('RefundService', 'refund', self.req)
    
    def update_voucher(self, voucher_info):
        if voucher_info:
            self.req['voucherInfo'] = str(voucher_info) if voucher_info else ''
            self.req['voucherAmount'] = voucher_info['amount']
            self.req['voucherId'] = voucher_info['vouId']

    def update_payContext(self, channel):
        if channel == 'alipay':
            self.req['payContext']['plugintype'] = '1'
        elif channel == 'wxpay':
            self.req['payContext']['plugintype'] = '0'
        elif channel == 'lianlianpay':
            self.req['payContext']
    
#     def create_direct_pay(self, channel, original_amount, pay_amount, ssoid=''):
#         '''
#         创建直扣订单
#         :param channel: wxpay alipay qqwallet
#         :param partner_order: 32位随机字符串
#         :param original_amount: 商品金额
#         :param pay_amount: 实付金额
#         :param ssoid: 为空，则取self.ssoid
#         '''
#         self.partner_order = RandomOrder(32).random_string()
#         self.req = {
#             'amount': pay_amount,
#             'partnerOrder': self.partner_order,
#             'partnerCode': self.partner_code,
#             'originalAmount': original_amount,
#             'ssoid': ssoid or GlobalVar.SSOID,
#             'channelType': self.channel_type,
#             'countryCode': 'CN', 'currency': 'CNY', 'productsName': 'TEST', "counts": "1",
#             'directPay': "ZHICHONG" if pay_amount else 'KB',
#             'payType': channel,
#             "tradeType": self.trade_type,
#             "contents": "", "mobileNum": "", "imei": "000000000000000", "imsi": "",
#             "ip": "127.0.0.1", "mac": "", "model": "PDCM00", "appPackage": "com.example.pay_demo", "appVer": "260",
#             "sdkVer": "1.0.0", "channelId": "", "gameType": "WANGYOU", "extra": "", "remark": "", "discountInfo": "",
#             "openid": "", "brandType": "OPPO", "mobileOsVer": "", "platform": "",
#             "screenInfo": "HALF", "factor": "", "notifyUrl": "www.baidu.com", "subPartnerOrders": [],
#             "kebiSpent": 0,
#             # SZF的话, 需要cardAmount,cardNo,cardPwd
#             # alipay: 1)plugintype, 取值有 0(其他如WAP), 1(APP支付)  
#             # wxpay: 1)plugintype, 取值有 0, NATIVE, JSAPI, APP 2)authorizationCode payWay是JSAPI时必填
#             "payContext": {"plugintype": "1"}
#         }
#         return self.conn.invoke('PayService', 'tryPay', self.req, flag='JSON')

#     def create_expend_pay(self, payType, originalAmount, amount, kb_spent, vou_amount,
#                           vou_original_amount, vou_id, partnerCode="2031",
#                           ssoid="2076075925", channelType="NATIVE", directPay="ZHICHONG", tradeType="PAY"):
#         '''
#             所有的金额都是元
#             channelType : NATIVE
#             directPay : ZHICHONG KB
#             payType: wxpay alipay
#             tradeType : PAY
#         '''
#         self.partner_order = RandomOrder(32).random_string()
#         self.req = {
#             'amount': amount,
#             'partnerOrder': self.partner_order,
#             'partnerCode': partnerCode,
#             # 合单指两个订单
#             'originalAmount': originalAmount,
#             'ssoid': ssoid,
#             'channelType': channelType,
#             'countryCode': 'CN', 'currency': 'CNY', 'productsName': 'TEST', "counts": "1",
#             'directPay': directPay,
#             'payType': payType,
#             "tradeType": tradeType,
#             "contents": "", "mobileNum": "", "imei": "000000000000000", "imsi": "",
#             "ip": "127.0.0.1", "mac": "", "model": "PDCM00", "appPackage": "com.example.pay_demo", "appVer": "260",
#             "sdkVer": "1.0.0", "channelId": "", "gameType": "WANGYOU", "extra": "", "remark": "", "discountInfo": "",
#             "openid": "", "brandType": "OPPO", "mobileOsVer": "", "platform": "",
#             "screenInfo": "HALF", "factor": "", "notifyUrl": "www.baidu.com", "subPartnerOrders": [],
#             "voucherAmount": vou_amount,
#             "voucherInfo": str({'vouId': vou_id, 'amount': vou_amount, 'price': vou_original_amount}),
#             "voucherId": vou_id, "kebiSpent": kb_spent,
#             "payContext": {"plugintype": "1"}
#         }
#         return self.conn.invoke('PayService', 'tryPay', self.req, flag='JSON')


def create_payorder_positive(case, partner_id='2031', **kwargs):
    paycenter_dubbo = PayCenterDubbo(partner_code=partner_id)
    result = paycenter_dubbo.create_payorder(case.originalAmount,
                                             case.amount,
                                             case.payType,
                                             kebi_spent=case.kebiSpent,
                                             voucher_info=case.voucherInfo or {},
                                             **kwargs
                                            )    
    if case.payType == 'alipay':
        return paycenter_dubbo.req, result
    try:
        choose_scarlett(case.amount, case.payType, result['payReqId'], partner_id=paycenter_dubbo.partner_code)
        """
        调用查询结果接口
        """
        start = time.perf_counter()
        while time.perf_counter() - start < 3:  # dubbo默认超时时间
            try:
                query_res = queryResult(result['payReqId'], pass_type="direct")
                # query_res=2001：tradeorder不存在，单支付中心接口下发时
                assert query_res in ('0000', '2001'), "%s not in ('0000', '2001')" %query_res
            except Exception as e:
                exc_inst = e
                time.sleep(1)
            else:
                break
        else:
            raise TimeoutError('查询支付结果超时3s，异常信息: %s!' %exc_inst)
        if is_assert():
            """
            检查order_info表信息是否正确
            """
            ASSERTION_IN.assert_order_info(paycenter_dubbo.ssoid, result['payReqId'], case.amount*100, case.amount*100)
    finally:
        return paycenter_dubbo.req, result


def create_payorder_negative(case, partner_id='2031', **kwargs):
    paycenter_dubbo = PayCenterDubbo(partner_code=partner_id)
    try:
        result = paycenter_dubbo.create_payorder(case.originalAmount,
                                                 case.amount,
                                                 case.payType,
                                                 kebi_spent=case.kebiSpent,
                                                 voucher_info=case.voucherInfo or {},
                                                 **kwargs
                                                )
    except:
        raise
    else:
        if paycenter_dubbo.conn.errmsg:
            print('Expected failed, PASS!')
            print('具体报错信息:', result)
            if case.expected:
                assert case.expected in result
            case.is_passed = 'passed'
        else:
            raise Exception('create_payorder expected failure, but passed')
    finally:
        return paycenter_dubbo.req, result
    

if __name__ == '__main__':
    set_global_env_id(1)
    paycenter_dubbo = PayCenterDubbo(ssoid='2086776969')
    # pay_req_id, channel_refund=0, kebi_refund=0, voucher_refund=0
    #paycenter_dubbo.refund_order("RM20210304095657207607592506772t", 10)
    # originalAmount, amount, kb_spent, vou_amout, vou_original_amount
    # payType, partnerOrder, originalAmount, amount, kebiSpent

    # 直扣订单
#     paycenter_dubbo.create_direct_pay("qqwallet", "0.01", "0.01")

    # 可币消费订单： 纯可币
#     paycenter_dubbo.create_payorder("", RandomOrder(32).random_string(), "0.01", "0", "0.01", directPay="KB")
    '''
    create_expend_pay(payType, originalAmount, amount, kb_spent, vou_amount,
                      vou_original_amount, vou_id, partnerCode="2031",
                      ssoid="2076075925", channelType="NATIVE", directPay="ZHICHONG", tradeType="PAY")
    '''
    # 可币消费订单：纯优惠券
    #paycenter_dubbo.create_payorder_vou("", RandomOrder(32).random_string(), "10.0", "0.0", "0", "10.0", "10.0", "20000", directPay="KB")

    # 可币纯消费： 可币 + 优惠券
    #paycenter_dubbo.create_payorder_vou("", RandomOrder(32).random_string(), "10.0", "0", "2", "8.0", "8.0", "20000", directPay="KB")

    # 充值消费：优惠券+可币+渠道（未通）
    #paycenter_dubbo.create_payorder_vou("alipay", RandomOrder(32).random_string(), "10.0", "1.0", "1", "8.0", "10.0", "20000")

    # 充值消费：优惠券+渠道
    #paycenter_dubbo.create_payorder_vou("alipay", RandomOrder(32).random_string(), "10.0", "2.0", "0", "8.0", "10.0", "20000")

    # 充值消费：可币+渠道
    #paycenter_dubbo.create_payorder("alipay", RandomOrder(32).random_string(), "10.0", "10.0", "0")

    # 加购订单

    # 退款
    # paycenter_dubbo.refund_order('KB202103021104132086100900705822', channel_refund=0.01, kebi_refund=0, voucher_refund=9.99)
