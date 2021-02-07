#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 22:54
# comment: 随机订单号
import time
import random
import string
from lib.common_biz.find_database_table import get_route_ssoid


class RandomOrder:
    def __init__(self, length):
        """
        :param length:
        """
        self.length = length

    def random_num(self):
        """
        生成随机数字字符串
        :return:
        """
        return ''.join(str(random.choice(range(10))) for _ in range(self.length))

    def random_string(self):
        """
        随机字符串
        :param length:
        :return:
        """
        return ''.join(random.sample(string.ascii_letters + string.digits, self.length))

    def business_order(self, business):
        """
        业务订单号，如：GC..../TV.../KB...
        格式：业务标识+时间戳+随机数
        :return:
        """
        return business + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + self.random_num()

    def coin_order(self, country, ssoid):
        """
        可币订单号生成规则，用于dubbo接口调用传入。订单查询接口依赖订单号的拆解，强制规则
        14位时间戳  + 10位ssoid + 5位随机数 + 一个机房标识
        测试环境无机房概念，直接随机1位
        ssoid不足10位数或大于10位，按照特定的规则生成
        :param country:
        :param ssoid:
        :return:
        """
        return country + time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + get_route_ssoid(
            ssoid) + self.random_num()


if __name__ == '__main__':
    print(len(RandomOrder(16).business_order("TV")))
    print(RandomOrder(6).coin_order("KB", "2076075925"))
