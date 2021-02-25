#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 22:53
# comment: 常见接口的签名拼接
from lib.common.file_operation.config_operation import Config
from lib.common.utils.meta import WithLogger
from lib.common_biz.file_path import join_sign_path
from lib.common.algorithm.md5 import md5


class Sign(metaclass=WithLogger):
    
    def __init__(self, original_dict):
        self.signString = ""
        self.original_dict = original_dict

    def join_delete_key_no_asc(self, section):
        """
        1. 需要删除部分字段 2.加盐串无需拼接key 3.无需按照ASCII码排序
        常用于md5算法
        e.g：skippy接口调用
        join_sign_key.ini文件中的value值，即为需要删除的字段
        :return:
        """
        section_sign = Config(join_sign_path).options(section)[0]
        list_delete_key = Config(join_sign_path).value_as_list(section, section_sign)
        # list_delete_key = json.loads(Config(join_sign_path).read_config(section, section_sign))
        # 循环遍历，删除需要删除的key（{"key":"value"}）
        for delete_key in list_delete_key:
            del self.original_dict[delete_key]
        for dict_value in self.original_dict.values():
            self.signString += dict_value
        return self.signString

    def join_asc_have_key(self, salt="", *args):
        """
        1. 按照ASCII码排序 2.格式为：参数名称=参数值，并用&连接 3.需要删除空的字段
        salt标识是否需要加 , 默认为空
        e.g : 解约接口
        注意：
            动态参数适用场景较少，支付宝的支付回调中，除了删除sign字段，还需要额外删除sign_type字段
        :return:
        """
        dataList = []
        for key in sorted(self.original_dict):
            if key in args or key == "sign" or self.original_dict[key] == '':
                continue
            dataList.append(("%s=%s" % (key, self.original_dict[key])))
        return "&".join(dataList) + salt

    def join_fixed_param(self, section, salt=""):
        """
        固定参数拼接, 拼接大小大小写不一致，不好写无法满足。
        可满足需要拼接的字符串与字典的key一致的情况
        e.g: 如：1. partnerId为字符串，字典里面是partnerid，不满足
                2. heeppay回调报文规范，可以使用该方法
        :return:
        """
        section_sign = Config(join_sign_path).options(section)[0]
        list_fixed_key = Config(join_sign_path).value_as_list(section, section_sign)
        for i in range(0, len(list_fixed_key)):
            # 在拼接字符的末尾是否加盐
            if i == len(list_fixed_key) - 1:
                self.signString = self.signString + list_fixed_key[i] + '=' + self.original_dict[list_fixed_key[i]]
                self.signString += salt
            else:
                self.signString = self.signString + list_fixed_key[i] + '=' + self.original_dict[list_fixed_key[i]] + '&'
        return self.signString

    def pb_common_sign_string(self, mp):
        """
        使用范围：
        1. 单机版本下单，签名字符拼接
        2. 与header同级sign
        :param mp:
        :return:
        """
        del self.original_dict['ip'], self.original_dict['sign']
        for item in self.original_dict:
            if isinstance(self.original_dict[item], str):
                self.signString = self.signString + str(self.original_dict[item])
            if isinstance(self.original_dict[item], dict):
                key = self.original_dict[item].keys()
                for i in key:
                    string_temp = str(i)
                    if i == 'sdkVer' or i == 'rate':
                        self.signString = self.signString + string_temp + ': ' + str(self.original_dict[item][i]) + '\n'
                    elif i == 'partnerorder' or i == "androidVersion":
                        self.signString = self.signString + string_temp + ': ' + '"' + str(self.original_dict[item][i]) + '"'
                    else:
                        self.signString = self.signString + string_temp + ': ' + '"' + str(self.original_dict[item][i]) + '"' + '\n'
        stringA = self.signString + mp
        return stringA
    
    def to_md5_sign(self, string):
        self.logger.info('sign original string: %s', string)
        return md5(string)


def expend_pay_sign_string(token, appPackage, partnerId, partnerOrder, productName, productDesc, price, count):
    """
    expend_pay(纯消费接口)签名字符串拼接
    :param token:
    :param appPackage:
    :param partnerId:
    :param partnerOrder:
    :param productName:
    :param productDesc:
    :param price:
    :param count:
    :return:
    """
    signString = ''
    signString = signString + 'token=\"' + token + '\"&'
    signString = signString + 'appPackage=\"' + appPackage + '\"&'
    signString = signString + 'partnerId=\"' + partnerId + '\"&'
    signString = signString + 'partnerOrder=\"' + partnerOrder + '\"&'
    signString = signString + 'productName=\"' + productName + '\"&'
    signString = signString + 'productDesc=\"' + productDesc + '\"&'
    signString = signString + 'price=\"' + str(price) + '\"&'
    signString = signString + 'count=\"' + str(count) + '\"'
    return signString


def simple_pay_sign_string(appPackage, partnerCode, partnerOrder, amount, payType):
    """
    simplepay签名字符串拼接
    :param appPackage:
    :param partnerCode:
    :param partnerOrder:
    :param amount:
    :param payType:
    :return:
    """
    signString = ''
    signString = signString + 'appPackage="' + appPackage + '"&'
    signString = signString + 'partnerCode="' + partnerCode + '"&'
    signString = signString + 'partnerOrder="' + partnerOrder + '"&'
    signString = signString + 'amount="' + amount + '"'
    signString = signString + 'payType="' + payType + '"'
    return signString


def auto_renew_sign_string(appPackage, partnerCode, signPartnerOrder, renewProductCode, amount, signAgreementNotifyUrl):
    """
    自动续费签名字符串拼接
    :param appPackage:
    :param partnerCode:
    :param signPartnerOrder:
    :param renewProductCode:
    :param amount:
    :param signAgreementNotifyUrl:
    :return:
    """
    signString = ''
    signString = signString + 'appPackage=\"' + appPackage + '\"&'
    signString = signString + 'partnerCode=\"' + partnerCode + '\"&'
    signString = signString + 'signPartnerOrder=\"' + signPartnerOrder + '\"&'
    signString = signString + 'renewProductCode=\"' + renewProductCode + '\"&'
    signString = signString + 'amount=\"' + amount + '\"&'
    signString = signString + 'signAgreementNotifyUrl=\"' + signAgreementNotifyUrl + '\"'
    return signString


def oversea_header_sign_string(version, token, model, apntype, package, r_v, sdkVer, appVerison):
    """
    生成海外baseheader头部签名字符串
    MD5运算
    :param version:
    :param token:
    :param model:
    :param apntype:
    :param package:
    :param r_v:
    :param sdkVer:
    :param appVerison:
    :return:
    """
    signString = ''
    signString = signString + version
    signString = signString + token
    signString = signString + model
    signString = signString + apntype
    signString = signString + package
    # r_v解码
    if isinstance(r_v, bytes):
        signString = signString + r_v.decode()
    else:
        signString = signString + r_v
    signString = signString + sdkVer
    signString = signString + appVerison
    return signString


def partner_key_sign_string(bizNo, developerId, appId, appName, appPublicKey, timestamp):
    """
    生成开发者密钥信息签名规则
    :return:
    """
    signString = ''
    signString = signString + 'bizNo' + bizNo
    signString = signString + 'developerId' + developerId
    signString = signString + 'appId' + appId
    signString = signString + 'appName' + appName
    signString = signString + 'appPublicKey' + appPublicKey
    signString = signString + 'timestamp' + timestamp
    return signString


def hee_pay_sign_string(scarlett_string):
    """
    骏网卡支付签名原始串
    :return:
    """
    md5_string = \
        "ret_code=" + scarlett_string["ret_code"] + "&" + "agent_id=" + scarlett_string['agent_id'] + "&" + "bill_id=" \
        + scarlett_string['bill_id'] + "&" + "jnet_bill_no=" + scarlett_string['jnet_bill_no'] + "&" + "bill_status=" +\
        scarlett_string["bill_status"] + "&" + "card_real_amt=" + scarlett_string['card_real_amt'] + "&" + \
        "card_settle_amt=" + scarlett_string["card_settle_amt"] + "&" + "card_detail_data=|||" + "574A4702E0644DA29E827E05"
    return md5_string


def coda_pay_sign_string(scarlett_string, api_key):
    """
    coda渠道签名原始串
    :param api_key: 配置中心配置key
    :param scarlett_string: 回调远串
    :return:
    """
    md5_string = scarlett_string['TxnId'] + api_key + scarlett_string['OrderId'] + scarlett_string['ResultCode']
    return md5_string


if __name__ == '__main__':
    a = {'bill_id': 'KB202101221511052076075925464312', 'agent_id': '1715258', 'sign': '', 'ret_msg': '-%b2%e9%d1%af%b4%a6%c0%ed', 'card_settle_amt': '0.00', 'ret_code': '0', 'bill_status': '1', 'card_real_amt': '50', 'jnet_bill_no': '|||0577208060631965370826174135'}
    print(Sign(a).join_fixed_param("hee_pay_scarlett", "&"))
