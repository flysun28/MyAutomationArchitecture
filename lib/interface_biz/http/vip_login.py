#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 22:56
# comment: 账号返回token接口
import os
import requests
import hmac
import hashlib
import json
from lib.common.file_operation.config_operation import Config
from lib.common.utils.meta import WithLogger
from lib.common_biz.file_path import account_path
from lib.common.session.http.http_json import HttpJsonSession
from lib.common.utils.globals import HTTPJSON_IN, GlobarVar

url = "http://i.auth.ucnewtest.wanyol.com/loging"
header = {"content-type": "application/json"}
appKey = "myKey"


class Vip(metaclass=WithLogger):
    
    def __init__(self):
        self.account_args = Config(account_path).as_dict("account")

    def login(self):
        """
        获取token
        :return:
        """
        m = hashlib.md5()
        m.update(self.account_args['password'].encode("utf8"))
        passWord_md5 = m.hexdigest()
        value = "{}{}{}".format(appKey, self.account_args['username'], passWord_md5).encode()
        sign = hmac.new(b"mySecret", value, hashlib.md5).hexdigest()
        body = "{{'appKey':'{}','loginName':'{}','passWord':'{}','sign':'{}'}}".format(appKey, self.account_args['username'], passWord_md5, sign)
        response = requests.post(url, data=body, headers=header)
        self.logger.info('返回的登录信息：{}'.format(response.json()))
        if response.json()['resultCode'] == '1700':
            self.logger.info('返回的异常登录信息：{}'.format(response.text))
        else:
            return response.json()['token']
    
    @staticmethod
    def get_verification_code(phone_number):
        """
        获取验证码
        :param phone_number:
        :return:
        """
        url = 'http://ucadmin.ucnewtest.wanyol.com/api/admin/account/autotest/query-latest-code'
        body = {"destination": phone_number}
        body = json.dumps(body)
        response = requests.post(url, data=body, headers=HttpJsonSession.header)
        print(response.status_code)
        print(response.json())


if __name__ == '__main__':
    a = Vip().login()
