#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/22 18:59
# comment:
import base64
import random


def random_int():
    randomInt = random.randint(0, 100)
    return randomInt


def trans_byte(src_bytes):
    """
    部分接口在序列化为二进制字节流后，做了以下转换，如simplepay，有些直接序列化后就可以组包发包，如skippay
    以下转化为：在二进制数据前增加4个字节，在其后增加两个字节，分别增加100以内随机数
    :return:
    """
    srcBytes = bytearray(src_bytes)
    randomInt = []
    for i in range(0, 6):
        randomInt.append(random_int().to_bytes(1, 'little'))
    randomBytes1 = randomInt[0] + randomInt[1] + randomInt[2] + randomInt[3]
    randomBytes2 = randomInt[4] + randomInt[5]
    des_bytes = randomBytes1 + srcBytes + randomBytes2
    return des_bytes


def convert_key(char_str):
    """
    以下方法对应客户端实现的生成r_v的算法
    :param char_str:
    :return:
    """
    byteArray = char_str.encode()
    asc = int(byteArray[0])
    return asc % 10


def extra_key(step_count, code_sign, sp_key):
    XLen = 10  # 二维数组x的长度
    YLen = 10  # 二维数组y的长度
    len_per = 8  # 每个二维数组值的长度
    if step_count + 2 > len(code_sign):
        stepCount = 0
    xPos = convert_key(code_sign[step_count] + "")
    yPos = convert_key(code_sign[step_count + 1] + "")
    stepCount = step_count + 2
    return sp_key[xPos * XLen + yPos * len_per: xPos * XLen + (yPos + 1) * len_per]


def get_RV(s_p, step_count=4):
    if s_p == '':
        return ""
    sp_key = base64.b64decode(s_p.encode('utf-8'))
    r_v = extra_key(4, s_p, sp_key)
    return str(r_v, encoding="utf-8")