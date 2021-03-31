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
import time
from lib.common.utils.meta import WithLogger
from lib.common.session.http.http_json import HttpJsonSession
from lib.common.utils.globals import GlobalVar
from lib.common_biz.sign import Sign
from lib.common.algorithm.md5 import md5
from lib.common.file_operation.config_operation import Config
from lib.config.path import key_configfile_path
from itertools import chain

header = {"content-type": "application/json"}
appKey = "myKey"


class Account(metaclass=WithLogger):
    
    def __init__(self):
        self.account_args = GlobalVar.TEST_ACCOUNT
        self.logger.info('账户信息: %s', self.account_args)
        self.user_account_key = Config(key_configfile_path).as_dict('user_account_key')
        self._ssoids = []

    def login(self):
        """
        获取token
        :return:
        """
        url = "http://i.auth.ucnewtest.wanyol.com/loging"
        m = hashlib.md5()
        m.update(self.account_args['pwd'].encode("utf8"))
        passWord_md5 = m.hexdigest()
        value = "{}{}{}".format(appKey, self.account_args['username'], passWord_md5).encode()
        sign = hmac.new(b"mySecret", value, hashlib.md5).hexdigest()
        body = "{{'appKey':'{}','loginName':'{}','passWord':'{}','sign':'{}'}}".format(appKey, self.account_args['username'], passWord_md5, sign)
        response = requests.post(url, data=body, headers=header)
        self.logger.info('返回的登录信息：{}'.format(response.json()))
        if response.json()['resultCode'] == '1700':
            self.logger.error('返回的异常登录信息：{}'.format(response.text))
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

    def get_basic_info(self):
        req = {
            'appKey': self.user_account_key['appkey'],
            'timestamp': int(time.time() * 10**3),
            'sign': '',
            'signType': 'md5',
            'userId': self.account_args['ssoid'],
            'userName': '',
            'mobile': '',
            'countryCallingCode': '',
            'email': ''
        }    
        result = GlobalVar.MYSQL_AUTO_TEST.select('SELECT username FROM `pay_auto_test_info`.`test_env_account`')
        orig_sign_str = Sign(req).join_asc_have_key('&key=') + self.user_account_key['priv_key']
        req['sign'] = md5(orig_sign_str, to_upper=False)
        result = GlobalVar.HTTPJSON_ACCOUNT_IN.post('/user/basic-info', data=req)
        assert result['success'] is True
        assert result['error'] is None
        return result['data']

    def get_all_ssoids(self):
        req = {
            'appKey': self.user_account_key['appkey'],
            'timestamp': int(time.time() * 10**3),
            'sign': '',
            'signType': 'md5',
            'userId': '',
            'userName': '',
            'mobile': '',
            'countryCallingCode': '',
            'email': ''
        }
        mobiles = GlobalVar.MYSQL_AUTO_TEST.select('SELECT username FROM `pay_auto_test_info`.`test_env_account`')
        mobiles = tuple(chain(*[d.values() for d in mobiles]))
        for mobile in mobiles:
            req['mobile'] = mobile
            orig_sign_str = Sign(req).join_asc_have_key('&key=') + self.user_account_key['priv_key']
            req['sign'] = md5(orig_sign_str, to_upper=False)
            result = GlobalVar.HTTPJSON_ACCOUNT_IN.post('/user/basic-info', data=req)
            try:
                assert result['success'] is True
                assert result['error'] is None
            except:
                pass
            else:
                self._ssoids.append(result['data']['userId'])
        print('所有ssoids:', self._ssoids)
    
    @property
    def all_test_ssoids(self):
        return self._ssoids


if __name__ == '__main__':
    a = Account().login()
#     print(Account().get_verification_code('18948606750'))