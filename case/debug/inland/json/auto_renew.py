#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/8 17:52
# comment:
from lib.common.algorithm.md5 import md5
from lib.common.utils.globals import GlobalVar
from lib.common_biz.find_key import GetKey, is_get_key_from_db
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign, old_wx_auto_renew
from lib.common.utils.constants import currency as country_currency


class AutoRenew:
    vip_renew_product_code = {
        'wxpay': '727243140023',
        'alipay': '727243140022'
    }
    partner_renew_product_code = {
        '2031': '20310001',
        '72724314': vip_renew_product_code,
        '247628518': '2476285180010'
    }
    
    def __init__(self, ssoid, partner_code='2031', renew_product_code=""):
        self.ssoid = ssoid
        self.partner_code = partner_code
        self.renew_product_code = renew_product_code
        if partner_code == '2031':
            self.renew_product_code = '20310001'
        self.renew_product_code = self.partner_renew_product_code[partner_code]

    def auto_renew_out(self, agreement_no, pay_type, third_part_id, amount=0.01):
        """
        向渠道发起扣费接口
        :return:
        """
        if isinstance(self.renew_product_code, dict):
            self.renew_product_code = self.renew_product_code[pay_type]
        case_dict = {
            'agreementNo': agreement_no,
            'ssoid': self.ssoid,
            'renewProductCode': self.renew_product_code,
            'partnerCode': self.partner_code,
            'partnerOrder': RandomOrder(32).random_string(),
            'payType': pay_type,
            'amount': amount,   #元
            'currencyName': 'CNY',
            'country': 'CN',
            'subject': '自动续费扣款',
            'desc': 'Default product desc...',
            'notifyUrl': 'http://pay.pay-test.wanyol.com/notify/notify/receiver',
            'apppackage': 'com.coloros.cloud',
            'thirdPartId': third_part_id,
            'imei': '',
            'model': '',
            'ip': '',
            'ext': '',
            'subUserId': '',
            # 签名未校验
            'sign': ''
        }
        # 业务方秘钥
        if is_get_key_from_db():
            merchant_key = GetKey(case_dict['partnerCode']).get_key_from_merchant()
        else:
            merchant_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCMVhIN5xQPRdmo1fmm0HBOlRk2XnJsuKgOBi6b1IFAUWtROpm6lRnw45M83a/XiHEZv5FOp+rssGlgwcWeLuexI6kCF5hFT6gsEYy9XRfpSBOUA2UwcajPRsMoEKRmEIm+NpmwnGAeeZK2Y7Xwr3imHdLJ86VgJ5zMedqd4IfXWQIDAQAB'        
        temp_string = Sign(case_dict).join_asc_have_key() + merchant_key
        case_dict['sign'] = md5(temp_string)
        GlobalVar.HTTPJSON_IN.post("/plugin/autorenew/autorenewpay", data=case_dict)

    def query_sign(self):
        """
        签约查询
        :return:
        """
        case_dict = {
            "ssoid": self.ssoid,
            "renewProductCode": self.renew_product_code,
            "partnerCode": self.partner_code,
            "currencyName": "CNY",
            "country": "CN",
            "sign": "efe9a9b2d3b058789cdd51ed007e5860"
        }
        GlobalVar.HTTPJSON_IN.post("/plugin/autorenew/querysign", data=case_dict)

    def un_sign(self, agreement_no, partner_order, pay_type):
        """
        解约。不适合微信，需手动，因测试环境的解约回调都去了生产。支付宝仅可在第一套环境，回调地址在支付宝配置死了。
        支付宝:调用接口解约，支付宝会回调到对应的地址。手动解约，是写死在支付宝侧的
        :return:
        """
        if isinstance(self.renew_product_code, dict):
            self.renew_product_code = self.renew_product_code[pay_type]
        case_dict = {
            'agreementNo': agreement_no,
            'ssoid': self.ssoid,
            'renewProductCode': self.renew_product_code,
            'partnerCode': self.partner_code,
            'partnerOrder': partner_order,
            'payType': pay_type,
            'currencyName': 'CNY',
            'country': 'CN',
            'apppackage': '',
#             'subUserId': '00001',    # 仅保险
            'sign': ''
        }
        temp_string = Sign(case_dict).join_asc_have_key() + GetKey(case_dict['partnerCode']).get_key_from_merchant()
        case_dict['sign'] = md5(temp_string)
        GlobalVar.HTTPJSON_IN.post("/plugin/autorenew/unsign", data=case_dict)
    
    def wx_unsign(self, xml):
        '''
        从首鸣获取微信解约回调原始xml报文
        e.g.
        '<xml>
            <change_type>DELETE</change_type>
            <contract_code>SN202106021010201133284552181126</contract_code>
            <contract_id>202106025390914093</contract_id>
            <contract_termination_mode>2</contract_termination_mode>
            <mch_id>1259634601</mch_id>
            <openid>oCg6Xt-0s4ns6EZ8ym0kW_JzUeps</openid>
            <operate_time>2021-06-02 11:14:53</operate_time>
            <plan_id>131584</plan_id>
            <request_serial>162259982077137627</request_serial>
            <result_code>SUCCESS</result_code>
            <return_code>SUCCESS</return_code>
            <return_msg>OK</return_msg>
            <sign>687F1195D53CECDB3D98E59E5B91C479</sign>
        </xml>'
        '''
        return GlobalVar.HTTPJSON_SCARLET.post('/opaycenter/wxpaysignnotify', data=xml)

    def old_unsign(self):
        req = {
            "ssoid": self.ssoid,
            "country": "CN",
            "partnerOrder": "OCLOUD-UNSIGN" + RandomOrder(20).random_num(),
            "payType": "alipay",
            "partnerCode": "231810428",
            "currencyName": "CNY",
            "agreementNo": "20215302717715435440",
            "apppackage": "com.coloros.cloud",
            "sign": "",
            # "alipayUserId":"2088332393982857"
            "alipayUserId": "2088112811111403"
        }
        temp_string = Sign(req).join_asc_have_key("&key=") + GetKey(req['partnerCode']).get_key_from_merchant()
        req['sign'] = md5(temp_string, to_upper=False)
        GlobalVar.HTTPJSON_IN.post("/plugin/oldautorenew/unsign", data=req)

    def wxpayavoidpay(self):
        """
        云服务老的代扣接口-微信
        :return:
        """
        req = {
            "t_p": "", "payorderid": "", "subject": "云服务空间购买", "desc": "云服务空间购买",
            "requestid": "OCLOUD" + RandomOrder(20).random_num() + "AUTO", "paytype": "", "amount": "0.01", "channelid": "", "notifyUrl": "https://aocloud.oppomobile.com/pay/v1/payNotify.json",
            "partnercode": "247628518", "appversion": "", "currencyName": "", "rate": "1", "imei": "", "model": "",
            "apppackage": "com.coloros.cloud", "mac": "", "sdkversion": "", "ip": "", "payVersion": "", "bankNo": "", "bankNm": "", "token": "", "isNeedExpend": "0",
            "ssoid": "2076064003", "payTypeRMBType": "", "type": "", "cardno": "", "cardpwd": "", "ext": "", "requestModel": "", "code": "", "mobile": "", "payrequestidOrder": "", "oriAmount": "", "ext1": "",
            "ext2": "202105025701133124",
            "sign": "", "showUrl": "", "discountInfo": ""
        }
        req['sign'] = md5(old_wx_auto_renew(req, "8m7djj32948d4ad6d822dxda12"), to_upper=False)
        GlobalVar.HTTPJSON_IN.post("/plugin/post/wxpayavoidpay", data="hai"+str(req)+"g")

    def alipayavoidpay(self):
        """
        云服务老的代扣接口-支付宝
        :return:
        """
        req = {
            "t_p": "", "payorderid": "",  "subject": "云服务空间购买", "desc": "云服务空间购买",
            "requestid": "OCLOUD" + RandomOrder(20).random_num() + "AUTO", "paytype": "",
            "amount": "0.01", "channelid": "", "notifyUrl": "https://aocloud.oppomobile.com/pay/v1/payNotify.json",
            "partnercode": "231810428", "appversion": "", "currencyName": "", "rate": "1", "imei": "", "model": "",
            "apppackage": "com.coloros.cloud", "mac": "", "sdkversion": "", "ip": "", "payVersion": "", "bankNo": "", "bankNm": "", "token": "", "isNeedExpend": "0",
            "ssoid": "2076064003", "payTypeRMBType": "", "type": "", "cardno": "", "cardpwd": "", "ext": "", "requestModel": "", "code": "", "mobile": "", "payrequestidOrder": "", "oriAmount": "", "ext1": "",
            "ext2": "{\"ALIPAY_USER_ID\":\"2088112811111403\",\"AGREEMENT_NO\":\"20215302717715435440\"}",
            "sign": "", "showUrl": "", "discountInfo": ""
        }
        req['sign'] = md5(old_wx_auto_renew(req, "8m7djj32948d4ad6d822dxda12"), to_upper=False)
        GlobalVar.HTTPJSON_IN.post("/plugin/post/alipayavoidpay", data="hai"+str(req)+"g")


class AutoRenewOverseas():
    
    def __init__(self, ssoid, country, partner_code='2031'):
        self.ssoid = ssoid
        self.country = country
        self.currency = country_currency[self.country]
        self.partner_code = partner_code

    def avoidpay(self, amount):
        '''
        自动续费
        e.g. {"ssoid":"621730086","amount":"1.28",
              "notifyUrl":"https://album-sg01a.ocloud.oppomobile.com/pay/v1/payNotify.json",
              "desc":"云服务空间购买","rate":"1","imei":"","model":"",
              "expectPayDate":"2021-05-31 08:10:22","lastPayDate":"2021-05-01 08:01:50",
              "country":"SG","currency":"SGD","sign":"f26796fd6550770553ee35657b322d9b",
              "apppackage":"com.coloros.cloud","requestid":"OCLOUD1622419222464K5262K621730086K128",
              "ext2":"B-4U833904UE160342K","subject":"云服务空间购买","partnercode":"247628518"
            }
        '''
        req = {"ssoid": self.ssoid,
               "amount": amount,
               "notifyUrl": "https://album-sg01a.ocloud.oppomobile.com/pay/v1/payNotify.json",
               "desc": "海外自动续费接口",
               "rate": "1",
               "imei": "",
               "model": "",
               "expectPayDate": "2021-06-02 17:30:00",
               "lastPayDate": "2021-05-01 08:01:50",
               "country": self.country,
               "currency": self.currency,
               "sign": "",
               "apppackage": "com.coloros.cloud",
#                "apppackage": "com.example.pay_demo",
               "requestid": RandomOrder(32).random_string(),    # partner_order
               "ext2": "B-6EA09242CR088031X",
               "subject": "海外自动续费接口",
               "partnercode": self.partner_code
        }
        app_priv_key = 'dfatd14s12830saw3jfmer9we0qk'   # 写死在海外pay-info的配置文件中，仅给云服务用
        orig_string = Sign(req).join_asc_have_key('&key='+app_priv_key)
        print('签名原串：', orig_string)
        req['sign'] = md5(orig_string, to_upper=False)
        GlobalVar.HTTPJSON_OUT.post('/avoid/avoidpay', data=req)


if __name__ == '__main__':
    flag = "1"
    if flag == "1":

        AutoRenewOverseas('2000060346', 'IN').avoidpay('100', )
#         AutoRenew('2000060346').auto_renew_out('202106025390914093', 'wxpay')
        AutoRenew('2086791398',"247628518","2476285180010").auto_renew_out('202106225829709435', 'wxpay', 'oCg6Xt8NvRi7jGuap_5B6XdY4oYk')
    if flag == "2":
        AutoRenew('2000060346').un_sign('') # agreement_no, partner_order, pay_type
    if flag == "3":
        AutoRenew().old_unsign()
    if flag == "4":
        AutoRenew().wxpayavoidpay()
    if flag == "5":
        AutoRenew().alipayavoidpay()

