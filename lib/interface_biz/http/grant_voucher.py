#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/9 23:42
# comment: 单张优惠券申请
import datetime
from lib.common.algorithm.md5 import md5
from lib.common.file_operation.config_operation import Config
from lib.common.utils.globals import GlobalVar
from lib.common_biz.file_path import key_path
from lib.common_biz.find_key import is_get_key_from_db, GetKey
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign
from lib.common.utils.env import set_global_env_id
end_time = str((datetime.datetime.now() + datetime.timedelta(days=365)).strftime('%Y-%m-%d %H:%M:%S'))


def grant_voucher(amount=1, vou_type=1, appId="2031"):
    """
    默认消费券
    :param appId: 
    :param vou_type: 
    :param amount: 分
    :return:
    """
    req = {
        "amount": amount,
        "appId": appId,
        "appSubName": "AUTO_TEST",
        "blackScopeId": "",
        "checkName": "TEST_ACCOUNT",
        "configId": "",
        "count": 1,
        "country": "CN",
        "currency": "CNY",
        "expireTime": end_time,
        "ext1": "",
        "ext2": "",
        "maxAmount": 1,
        "name": "AUTO_TEST",
        "partnerOrder": RandomOrder(28).business_order("AUTO"),
        "ratio": "",
        "remark": "",
        "salePrice": 0,
        "scopeId": "7104f7bc23e445daba913a5a96a264ac",
        "settleType": 1,
        "sign": "",
        "ssoid": GlobalVar.SSOID,
        "subScopeId": "",
        "timezone": "",
        # 1 消费券
        "type": vou_type,
        "useableTime": "2021-01-01 00:00:00"
    }
    key = ''
    if is_get_key_from_db:
        key = GetKey(req['appId']).get_key_from_voucher()
    else:
        key = Config(key_path).as_dict('oversea_vou_app_info')["key_" + req['appId']]
    req['sign'] = md5(Sign(req).join_asc_have_key("&key=") + key)
    result = GlobalVar.HTTPJSON_IN.post("/voucher/grantSingle", data=req)
    # 返回优惠券id
    return result['vouIdList'][0]


class GrantMultiVous():
    
    def __init__(self, ssoid, partner_id):
        self.ssoid = ssoid
        self.appid = partner_id
        self.vou_info = []
    
    def update_vou_info(self, voutype, name, count, amount, max_amount):
        

def grant_multi_vouchers(ssoid, partner_id, *vouinfos):
    '''
    按照用户维度，批量发不同类型的券
    :param ssoid: 账户id
    :param partner_id: 业务线id
    :请求参数列表：
    字段          类型        含义        必要性
    ssoid       String      用户ID           Y
    country     String    二位字母的国家代码   N
    timezone    String    UTC时区            N
    currency    String    三位字母的币种      N
    appId       String    业务线ID           Y    
    requestId   String    请求ID            Y
    sign        String    签名              Y
    grantVoucherInfoList    List<GrantVoucherInfo>    Y
        vouType    String    券优惠类型                Y
        vouName    String    优惠券名称                Y
        grantCount    Integer    发放数量              Y
        amount    BigDecimal    金额,元    
        maxAmount    BigDecimal    金额,元    
        ratio    BigDecimal    打折的折扣    打折券使用
        beginTime    Long    允许使用的开始时间         Y
        expireTime    Long    允许使用的结束时间        Y
        scopeId    String    使用范围ID                Y
        subScopeId    String    子范围ID              N
        blackScopeId    String    黑名单范围ID         N
        settleType    String    结算类型               Y
        batchId    String    批次号                    N
    '''
    req = {
        'ssoid': ssoid,
        'country': '',
        'timezone': '',
        'currency': '',
        'appId': partner_id,
        'requestId': '',
        'sign': '',
        'grantVoucherInfoList': []
    }
    if is_get_key_from_db:
        priv_key = GetKey(req['appId']).get_key_from_voucher()
    else:
        priv_key = Config(key_path).as_dict('oversea_vou_app_info')["key_" + req['appId']]
    orig_sign_str = Sign(req).join_asc_have_key("&key=") + priv_key
    req['sign'] = md5(orig_sign_str, to_upper=False)
    result = GlobalVar.HTTPJSON_IN.post("/voucher/grantMultiVoucher", data=req)


if __name__ == '__main__':
#    print(grant_voucher())
   set_global_env_id(3)
   grant_multi_vouchers('2086100900', '2031')