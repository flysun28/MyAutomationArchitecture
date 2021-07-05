'''
Created on 2021年6月4日
@author: 80319739
'''
from .misc_utils import to_pinyin
from bidict import bidict


currency = {
    "CN": "CNY",
    "VN": "VND",
    "PH": "PHP",
    "TW": "TWD",
    "ID": "IDR",
    "MY": "MYR",
    "IN": "USD",
    "TH": "THB",
}

rate_coin = {
    "VND": 250.000000,
    "PHP": 0.500000,
    "TWD": 0.320000,
    "IDR": 160.000000,
    "MYR": 0.040000,
    "INR": 0.800000,
    "THB": 0.320000
}

# 1消费 2抵扣 5折扣 7消费折扣 8红包
voucher_type_enum = {
    '消费': '1',
    '抵扣': '2',
    '折扣': '5',
    '消费折扣': '7',
    '红包': '8'
}
for k, v in voucher_type_enum.copy().items():
    voucher_type_enum.setdefault(to_pinyin(k, heteronym=False), v)
    voucher_type_enum.setdefault(to_pinyin(k, heteronym=False).upper(), v)

voucher_enum_to_type = {
    '1': '消费',
    '2': '抵扣',
    '5': '折扣',
    '7': '消费折扣',
    '8': '红包'
}
for k, v in voucher_enum_to_type.copy().items():
    voucher_enum_to_type.setdefault(int(k), v)
    
voucher_type_mapping = bidict({
    '1': '1',
    '2': '2',
    '5': '3',
    '7': '4',
    '8': '8'
})


app_packages = 'com.example.pay_demo', 'com.oppo.usercenter'