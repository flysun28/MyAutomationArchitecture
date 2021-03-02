'''
Created on 2021年2月26日
@author: 80319739
'''
import pandas
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.env import get_dubbo_info, set_global_env_id


class PayCenterDubbo():
    
    def __init__(self):
        dubbo_info = get_dubbo_info("pay_biz_paycenter")
        self.conn = DubRunner(*dubbo_info)
    
    def create_payorder(self, partner_order, partner_code, original_amount, products_name, 
                        amount=0, kebi_spent=0, voucher_info={}, **kwargs):
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
        | payType          | 选填 |    String     |                  | 支付方式        
        | directPay        | 选填 |    String     |  
        | presentAmount    | 选填 |    String     |                  | amount, kebiSpent, voucherAmount不能同时为空
        | countryCode      | 选填 |    timestamp  |      
        | currency         | 选填 |    timestamp  |  
        | kebiSpent        | 选填 |    Long       |                  | 可币支付金额，amount, kebiSpent, voucherAmount不能同时为空
        | voucherAmount    | 选填 |    BigDecimal |                  | 优惠券金额，voucherAmount 和 voucherInfo 需同时共存
        | voucherInfo      | 选填 |    String     |                  | 优惠券信息JSON串
        | voucherId        | 选填 |    String     |                  |
        | tradeType        | 选填 |    String     | KB 或者 ZHICHONG  | 仅用于生成兼容的PayReqID, ZHICHONG 的话, payReqId开头字母为KB, 其余的话, 均为RM    
        | contents         | 选填 |    String     |                  | 商品介绍
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
        | factor           | 选填 |    String     |   
        | notifyUrl        | 选填 |    String     |   
        | subPartnerOrders | 选填 |  List<String> |           | 合单的子订单号列表 |        

        '''
#         table = pandas.read_html('https://doc.myoas.com/display/pingtai/pay-biz-paycenter+PayService',
#                                  encoding='utf-8')[0]
#         print(table)
        req = {
            'partnerOrder': partner_order,
            'partnerCode': partner_code,
            'originalAmount': original_amount,
            'amount': amount,
            'productsName': products_name,
            'counts': '1',
            'ssoid': '2086100900',
            'channnelType': '',
            'payType': '',
            'directPay': '',
            'presentAmount': '',
            'countryCode': '',
            'currency': '',
            'kebiSpent': kebi_spent,
            'voucherAmount': '',
            'voucherInfo': str(voucher_info),
            'voucherId': '',
            'tradeType': '',
            'contents': '',
            'mobileNum': '',
            'imei': '',
            'imsi': '',
            'ip': '',
            'mac': '',
            'model': '',
            'appPackage': '',
            'appVer': '',
            'sdkVer': '',
            'channelId': '',
            'gameType': '',
            'extra': '',
            'remark': '',
            'discountInfo': '',
            'openid': '',
            'brandType': '',
            'mobileOsVer': '',
            'platform': '',
            'screenInfo': '',
            'factor': '',
            'notifyUrl': '',
            'subPartnerOrders': []
        }
        if voucher_info:
            req['voucherAmount'] = voucher_info['cutAmount']
            req['voucherId'] = voucher_info['id']
        req.update(kwargs)
        self.conn.invoke('PayService', 'tryPay', req, flag='SINGLE_STRING')
        
    def refund_order(self, pay_req_id, channel_refund=0, kebi_refund=0, voucher_refund=0, **kwargs):
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
        req = {
            'refundId': '',
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
        req.update(kwargs)
        self.conn.invoke('RefundService', 'refund', req, flag='SINGLE_STRING')


if __name__ == '__main__':
    set_global_env_id(3)
    paycenter_dubbo = PayCenterDubbo()
    # 直扣
    paycenter_dubbo.create_payorder('9f5a03cfc916433a806d057f9a1d7b11', '2031', 10.01, '\\', amount=0.01)
    # 可币券+渠道
#     paycenter_dubbo.create_payorder('9f5a03cfc916433a806d057f9a1d7b11', '2031', 10.01, '\\', 
#                                     amount=0.01, kebi_spent=0, voucher_info={"cutAmount":"1000", "id":"64234483", "type":"2"}, )
    # 退款
#     paycenter_dubbo.refund_order('KB202103021104132086100900705822', channel_refund=0.01, kebi_refund=0, voucher_refund=9.99)
    