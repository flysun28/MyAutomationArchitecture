#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/6/24 11:24
# comment:

import hashlib
import json
import random
import time
import requests


def sign_string(data):
    """
    gateway外部sign字段字符串构造
    :param data: 需要签名的数据，字典类型
    :return: 处理后的字符串， 格式为：参数名称=参数值，并用&连接
    """
    dataList = []
    for k in sorted(data):
        if k == 'sign':
            continue
        dataList.append(("%s=%s" % (k, data[k])))
    return "&".join(dataList)


def get_random_number(length):
    """
    生成随机数字字符串
    :param length: 字符串长度
    :return:
    """
    num_str = ''.join(str(random.choice(range(10))) for _ in range(length))
    return num_str


def md5_sign(data, key):
    """
    MD5签名
    :param data: MD5签名需要的字符串
    :param key: 签名需要的key
    :return:
    """
    data = sign_string(data) + key
    md5 = hashlib.md5()
    md5.update(data.encode("utf-8"))
    return md5.hexdigest()

#  测试
# key = 'e3bf9782ef8c4706bf3ccaa5eea908da'
# url = 'http://pay-gateway.pay-overseas-test.wanyol.com/gateway/activity-repacket-grant'

# 生产
key = 'e3bf9782ef8c4706bf3ccaa5eea908da'
url = 'http://pay-gateway.pay-overseas-test.wanyol.com/gateway/activity-repacket-grant'

# case_dict = {
#     'charset': 'UTF8',
#     'format': 'JSON',
#     'bizContent': "{'ssoid': '2076075925', 'packetId': '0d151efdfbf8429ca9ca557fbb9f5b40', 'appPackage': "
#                   "'com.skymoons.hqg.nearme.gamecenter', 'beneficiaryAccountNo': '918008484891', 'userClientIp': "
#                   "'192.168.1.1', 'amount': '1.01', 'loginId': '13590362606', 'callBackUrl': "
#                   "'http://10.13.33.120:18842/sdklocal/withdraw/order/v1/redPackCallBack', 'beneficiaryPhoneNo': "
#                   "'8448197836', 'userId': 'oCg6Xt7DCpBt6arZxjvVtFSlBPW0', 'beneficiaryIFSC': 'PYTM0123456', "
#                   "'bizActivityId': '315', 'beneficiaryEmail': '', 'requestId': '53690883651468675659485640317607', "
#                   "'imei': '869541029924076', 'partnerId': '2031'}",
#     'version': '1.0',
#     'sign_type': 'MD5',
#     'app_id': '100001',
#     'timestamp': '2020-08-07 17:58:21',
#     'sign': ''
# }

# 'beneficiaryAccountNo': '918008484891'， 'beneficiaryIFSC': 'PYTM0123456'， 'loginId': '13590362606'

case_dict = {'charset': 'UTF8', 'format': 'JSON', 'bizContent': {
    'ssoid': '2076075925',
    'packetId': 'ef3abe4999a64aa79d93dd46a1113ca7',
    'appPackage': 'com.skymoons.hqg.nearme.gamecenter',
    'beneficiaryAccountNo': '',
    'userClientIp': '192.168.1.1',
    'amount': '2',
    'loginId': '13590362606',
    'callBackUrl': 'http://10.13.33.120:18842/sdklocal/withdraw/order/v1/redPackCallBack',
    # 吉喆账号
    'beneficiaryPhoneNo': '8448197836',
    'userId': 'oCg6Xt7DCpBt6arZxjvVtFSlBPW0',
    'beneficiaryIFSC': '',
    'bizActivityId': '29',
    'beneficiaryEmail': '',
    'requestId': '',
    'imei': '869541029924076',
    'partnerId': '100001'
}, 'version': '1.0', 'sign_type': 'MD5', 'app_id': '100001', 'timestamp': '2020-03-10 15:34:01', 'sign': ''}

case_dict['bizContent']['requestId'] = get_random_number(32)

# timestamp时间戳替换
case_dict['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
# bizContent 传输方式为字符串类型
case_dict['bizContent'] = str(case_dict['bizContent'])
# 签名替换
if case_dict['sign'] == '':
    case_dict['sign'] = md5_sign(case_dict, key).upper()
print('传入的参数{}'.format(case_dict))
# 发送http请求
result = requests.post(url, data=json.dumps(case_dict))
print('返回结果：', result.json())
