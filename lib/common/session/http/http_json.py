#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/22 19:11
# comment:
import requests
import json
from requests.exceptions import RequestException
from simplejson.errors import JSONDecodeError
from lib.common.utils.meta import WithLogger
from lib.common.exception import HttpJsonException


class HttpJsonSession(metaclass=WithLogger):
    header = {'Content-Type': 'application/json;charset=utf-8',
              'Connection': 'keep-alive',
              'Accept-Encoding': 'gzip, deflate',
              'Accept': '*/*',
              'User-Agent': 'HttpJson/1.0'
              }

    def __init__(self, url_prefix=None, data=None, **kwargs):
        """
        :param url: 请求地址
        :param data: 请求参数
        """
        self.prefix = url_prefix if url_prefix else ''
        self.url = ''
        self.data = data
        self.session = requests.Session()
        self.header.update(kwargs)
        self.session.headers = self.header

    def post(self, url, data=None):
        self.url = self.prefix + url
        data = data or self.data
        try:
            self.logger.info("传入的参数：{}".format(data))
            response = self.session.post(url=self.url, data=json.dumps(data))
            self.logger.info("返回状态码{}, 返回结果：{}".format(response.status_code, response.json()))
            return response.json()
        except RequestException as e:
            raise HttpJsonException(e) from None        
        except AssertionError:
            raise AssertionError('%s POST response:\n%s' %(self.url, response)) from None
        except:
            raise

    def get(self, data=None):
        data = data or self.data
        try:
            response = self.session.get(url=self.url, params=json.dumps(data))
            self.logger.info(response)
            return response.json()
        except RequestException as e:
            raise HttpJsonException(e) from None

    def close(self):
        self.session.close()


HttpJson = HttpJsonSession
