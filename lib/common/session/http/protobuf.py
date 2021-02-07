#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/22 18:57
# comment:
import requests
from lib.common.algorithm.other import trans_byte
from lib.common.utils.meta import WithLogger
from lib.common_biz import pbjson


class ProtoBuf(metaclass=WithLogger):
    def __init__(self, file_name):
        """
        :param file_name: pb-python文件
        """
        self.file_name = file_name

    def runner(self, url, request, case, header=None, flag=1):
        """
        pb请求
        :param header:
        :param url: 请求的url地址
        :param request: 请求方法
        :param case: 测试用例
        :param flag: 是否需要加随机字节标志位置
        :return:
        """
        NAME = pbjson.dict2pb(getattr(self.file_name, request), case)
        try:
            src_data = NAME.SerializeToString()
        except Exception as e:
            self.logger.info("序列化异常，{}".format(e))
        if flag:
            self.logger.debug('无需加入随机字节，标志位：1')
            self.logger.info('传入的参数：{}'.format(NAME))
            response = requests.post(url, src_data, headers=header)
            return response
        elif flag == 0:
            self.logger.debug('需加入随机字节，标志位：0')
            self. logger.info('传入的参数：{}'.format(NAME))
            des_data = trans_byte(src_data)
            response = requests.post(url, des_data, headers=header)
            return response
        else:
            self.logger.info('是否需要加随机字节标志位置不正确，请重新输入')

    def parser(self, method, response):
        """
        pb回参解析
        :param method:
        :param response:
        :return:
        """
        result = getattr(self.file_name, method)()
        try:
            result.ParseFromString(response.content)
            self.logger.info('返回的参数{}'.format(result))
        except Exception as e:
            self.logger.info("回参异常:{}".format(e))
        return result


if __name__ == '__main__':
    pass
    # from pb_src.python_native import ExpendPayPb_pb2
    # url = "http://pay.pay-test.wanyol.com/plugin/post/expendpay"
    # data_dict = {'header': {'version': '6.0', 't_p': 'd78380e5aa2145d3a9c72f5f4bba542f', 'imei': '', 'model': 'PCRM00', 'apntype': '1', 'package': 'com.example.pay_demo', 'r_v': b'mJZ4zmGL', 'ext': '', 'sdkVer': 209, 'country': 'CN', 'currency': 'CNY', 'openId': '', 'brandType': 'OPPO', 'mobileos': '17', 'androidVersion': '29', 'appVerison': '3.1.5'}, 'price': 1, 'count': 1, 'productname': 'test', 'productdesc': 'test', 'partnerid': '2031', 'callBackUrl': 'http://secure.pay-test2.wanyol.com/notify/receiver', 'partnerOrder': 'wKWjBGZJ3DhMXt82IFCkYdiOAq14aeQl', 'channelId': 'demo', 'ver': '3.1.5', 'source': 'test', 'attach': '', 'sign': b'UkxoI5JAzUimMdAQ8A6HcoohWfeEi4/QxbTL9xkzHu1gFVxxZjclj/5HYMRM2LaAkbMYPEC1d/MdJcSGUbpbC5eKZBpluRgWwfxZ7aFBq2/UrJL90L2+8MuxCz+zIR6scncCSUGla5lLS1JFA06gAJlEuQmFWtIa/PhKCPd+0Qg=', 'order': '2021012219571', 'ip': '120.197.148.147', 'factor': ''}
    # response = ProtoBuf(ExpendPayPb_pb2).runner(url, 'request', data_dict, flag=0)
    # result = ProtoBuf(ExpendPayPb_pb2).parser('Result', response)