#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/8 16:43
# comment:
import time

from lib.common.algorithm.md5 import md5
from lib.common.utils.globals import GlobarVar
from lib.common_biz.find_key import GetKey
from lib.common_biz.order_random import RandomOrder
from lib.common_biz.sign import Sign


class RedPacket:

    def __init__(self):
        pass

    def red_packet_inland(self):
        case_dict = {
            'charset': 'UTF8',
            'format': 'JSON',
            'bizContent': {
                'ssoid': '2076075925',
                'packetId': 'bwjCO1A0lIjw8vI28Jaz-OoQJgoUejmDHWLPD0ppS-Ksn4ge4wBRFkiLOjq1h1Jd',
                'appPackage': 'com.skymoons.hqg.nearme.gamecenter',
                'userClientIp': '192.168.1.1',
                'amount': '0.2',
                'loginId': '',
                'callBackUrl': 'http://pay.pay-test.wanyol.com/notify/receiver',
                # 优先userid
                'userId': '2088112811111403',
                'bizActivityId': '203951',
                'requestId': RandomOrder(32).random_num(),
                'imei': '869541029924076',
                'partnerId': '111111111'
            },
            'version': '1.0',
            'sign_type': 'MD5',
            'app_id': '100001',
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'sign': ''
        }
        case_dict['bizContent'] = str(case_dict['bizContent'])
        temp_string = Sign(case_dict).join_asc_have_key() + GetKey(case_dict['app_id']).get_key_from_server_info()
        case_dict['sign'] = md5(temp_string)
        GlobarVar.HTTPJSON_GW_IN.post("/gateway/activity-repacket-grant", data=case_dict)

    def red_packet_overseas(self):
        pass


if __name__ == '__main__':
    RedPacket().red_packet_inland()