'''
Created on 2021年6月1日

@author: 80319739
'''

from lib.common.utils.globals import HTTPENCJSON_IN


req = {
    'payRequestId': 'KB20210528155558208677696970137t'
}

result = HTTPENCJSON_IN.post('/api/pay-flow/v290/query-pay-result', req)

'''
data    object    非必须
    orderStatus    string    非必须    订单状态枚举 OK / FAIL / INIT    
    originAmount    integer    非必须 原始订单金额，单位分    
    amount    integer    非必须 实际支付金额，单位分    
    presentAmount    integer    非必须 优惠金额，单位分    
    payType    string    非必须 支付方式
'''
print(result)

