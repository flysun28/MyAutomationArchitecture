'''
Created on 2021年8月4日
@author: 80319739
'''
import time
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.globals import GlobalVar
from lib.common_biz.order_random import RandomOrder
from lib.common.utils.meta import WithLogger
from lib.common.algorithm.md5 import md5
from lib.common.file_operation.config_operation import Config
from lib.common_biz.sign import Sign
from lib.common_biz.file_path import key_path
from lib.interface_biz.scarlett.json_to_xml import wx_normal_pay_to_xml


class ScarletToPayCenterCallBack(metaclass=WithLogger):
    '''
    构造从Scarlett路由到Paycenter的回调dubbo报文
    Mock目的：不依赖于Scarlett服务，与渠道回调完全解耦
    '''
    def __init__(self):
        self.node = 'com.oppo.pay.paycenter.facade' 
        server_info = GlobalVar.ZK_CLIENT_IN.get_node_info(self.node)
        self.conn = DubRunner(server_info['ip_port'][0], server_info['ip_port'][1])
        self.base_req = {
            'payReqId': '',
            'success': True,
            'successTime': time.strftime('%Y-%m-%dT%H:%M:%S'),   # e.g. 2021-08-04T09:14:36
            'amount': 0
        }
        
    def _notify_by_pay_result(self, data):
        result = self.conn.invoke(
            "PayService",
            "notifyByPayResult",
            data
        )


class AliScarlettToPayCenter(ScarletToPayCenterCallBack):
    
    def _make_chl_to_scarlett_json(self, pay_req_id, price, merchant_no, trade_status="TRADE_SUCCESS")->dict:
        to_scarlett_info = {
            "gmt_create": time.strftime('%Y%m%d%H%M%S', time.localtime()),
            "buyer_email": "157****2782",
            "notify_time": time.strftime('%Y%m%d%H%M%S', time.localtime()),
            "seller_email": 'kekezhifu@keke.cn',
            "quantity": "1",
            "subject": "支付宝支付",
            "use_coupon": "N",
            "sign": "",
            "discount": "0.00",
            "body": "支付宝支付",
            "buyer_id": "2088612982416601",
            "notify_id": RandomOrder(32).random_num(),
            "notify_type": "trade_status_sync",
            "payment_type": "1",
            "out_trade_no": pay_req_id,
            "price": price,
            "trade_status": trade_status,
            "total_fee": price,
            "trade_no": RandomOrder(28).random_num(),
            "sign_type": "RSA",
            "seller_id": merchant_no,
            "is_total_fee_adjust": "Y"
        }
        self.logger.info("回调参数：{}".format(to_scarlett_info))
        # key自行生成，存放在配置文件中
        to_scarlett_info['sign'] = md5(Sign(to_scarlett_info).join_asc_have_key("", "sign_type") +
                                    Config(key_path).read_config("key_private_ali", "value"))
        return to_scarlett_info
    
    def notify_by_pay_result(self, pay_req_id, amount, merchant_no:str):
        '''       
        alipay，从Scarlett到paycenter的dubbo接口
        :param pay_req_id:
        :param amount:
        :param chl_ret_msg:
        :param merchant_no:
        '''
        data = {}
        base_req = {
            'payReqId': pay_req_id,
            'success': True,
            'successTime': time.strftime('%Y-%m-%dT%H:%M:%S'),   # e.g. 2021-08-04T09:14:36
            'amount': amount
        }
        scarlet_json = self._make_chl_to_scarlett_json(pay_req_id, amount, merchant_no) 
        chlRetRawMsg = '&'.join(scarlet_json.values())
        chl_result_req = {
            'notifyId': '',
            'chlRetRawMsg': chlRetRawMsg,
            'chlRetCode': None,
            'chlRetMsg': None,
            'merchantNo': scarlet_json.get('seller_id'),
            'channelUserId': scarlet_json.get('buyer_id'),
            'overridePayType': None
        }
        data.update(base_req, **chl_result_req)
#         data.update(payContext={})    # payContext会在notifyByPayResult中update
        self._notify_by_pay_result(data)


class WxScarlettToPayCenter(ScarletToPayCenterCallBack):
    
    def _make_chl_to_scarlett_json(self, mch_id, pay_req_id, appid, total_fee, 
                                  trade_type="APP", attach="TEST", result_code="SUCCESS", return_code="SUCCESS"):
        return {
            "transaction_id": RandomOrder(28).random_num(),
            "nonce_str": RandomOrder(32).random_string(),
            "bank_type": "OTHERS",
            "openid": "oCg6Xt8NvRi7jGuap_5B6XdY4oYk",
            "sign": "",
            "fee_type": "CNY",
            "mch_id": mch_id,
            "cash_fee": "1",
            "out_trade_no": pay_req_id,
            "appid": appid,
            "total_fee": total_fee,
            "trade_type": trade_type,
            "result_code": result_code,
            "attach": attach,
            "time_end": time.strftime('%Y%m%d%H%M%S', time.localtime()),
            "is_subscribe": "N",
            "return_code": return_code
        }
    
    def notify_by_pay_result(self, pay_req_id, amount, merchant_no:str, appid, md5_key):
        data = {}
        base_req = {
            'payReqId': pay_req_id,
            'success': True,
            'successTime': time.strftime('%Y-%m-%dT%H:%M:%S'),   # e.g. 2021-08-04T09:14:36
            'amount': amount
        }
        wx_scarlett = self._make_chl_to_scarlett_json(merchant_no, pay_req_id, appid, amount)
        chlRetRawMsg = wx_normal_pay_to_xml(wx_scarlett, md5_key)
        chl_result_req = {
            'notifyId': '',
            'chlRetRawMsg': chlRetRawMsg,
            'chlRetCode': None,
            'chlRetMsg': None,
            'merchantNo': wx_scarlett['mch_id'],
            'channelUserId': wx_scarlett['openid'],
            'overridePayType': None
        }
        data.update(base_req, **chl_result_req)
#         data.update(payContext={})    # payContext会在notifyByPayResult中update
        self._notify_by_pay_result(data)


if __name__ == '__main__':
    AliScarlettToPayCenter().notify_by_pay_result(pay_req_id, 0.01, merchant_no)
#     WxScarlettToPayCenter().notify_by_pay_result()

