#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/22 19:11
# comment:
import json
import requests
import simplejson
import time
import chardet
import base64
import sys
from copy import deepcopy
from urllib.parse import quote
from requests.exceptions import RequestException
from lib.common.utils.meta import WithLogger
from lib.common.exception import HttpJsonException
from lib.common_biz.sign import Sign
from lib.common.utils.misc_utils import create_random_str
from lib.common.file_operation.config_operation import Config
from lib.config.path import key_configfile_path
from lib.common.algorithm.aes import AES4J
from lib.common.algorithm.other import str_to_base64
from lib.common.algorithm.cipher import RSA
from lib.common_biz.file_path import encjson_rsa_public_key_path
from lib.common.algorithm.md5 import md5


class HttpJsonSession(metaclass=WithLogger):
    header = {'Content-Type': 'application/json;charset=utf-8',
              'Connection': 'keep-alive',
              'Accept-Encoding': 'gzip, deflate',
              'Accept': '*/*',
              'User-Agent': 'HttpJson/1.0'
              }

    def __init__(self, url_prefix=None, data: dict = None, **kwargs):
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
#         self.logger.info('HTTP Header: %s', self.session.headers)

    def post(self, url, data: dict = None):
        self.url = self.prefix + url
        data = data or self.data
        try:
            self.logger.info(self.url)
            self.logger.info("传入的参数：{}".format(data))
            response = self.session.post(url=self.url, data=simplejson.dumps(data))
            self.logger.info("返回状态码：{}".format(response.status_code))
            assert response.status_code == 200, "返回状态码：{} != 200".format(response.status_code)
            result = response.json()
            try:
                if result['code'] != '0000':
                    result['request'] = data
            except KeyError:
                pass
            self.logger.info("返回结果：{}".format(result))
            return result
        except RequestException as e:
            raise HttpJsonException(e) from None
        except AssertionError:
            raise AssertionError('%s POST response:\n%s' % (self.url, response)) from None
        except:
            raise

    def get(self, url, data: dict = None):
        self.url = self.prefix + url
        data = data or self.data
        try:
            self.logger.info(self.url)
            self.logger.info("传入的参数：{}".format(data))
            response = self.session.get(url=self.url, **data)
            self.logger.info("返回状态码：{}".format(response.status_code))
            assert response.status_code == 200, "返回状态码：{} != 200".format(response.status_code)
            self.logger.info("返回结果：{}".format(response.json()))
            return response.json()
        except RequestException as e:
            raise HttpJsonException(e) from None
        except AssertionError:
            raise AssertionError('%s POST response:\n%s' % (self.url, response)) from None
        except:
            raise

    def close(self):
        self.session.close()


HttpJson = HttpJsonSession


class EncryptJson(HttpJsonSession):
    req_header = {
        'Content-Type': 'application/encrypted-json;charset=utf-8',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'application/encrypted-json;charset=utf-8',
        'User-Agent': 'EncryptJson/1.0',
        'X-Protocol-Ver': '3.0',
        'X-Protocol': {'key': '',  # RSA公钥加密后的sessionKey
                       'iv': '',  # key对应的随机iv信息
                       # 会话秘钥，服务端用对称私钥加密sessionKey后的产物，由服务端回传给客户端，下一次通讯用该字段代替sessionKey
                       'sessionTicket': ''
                       },
        'X-SDK': {'sdkBuildTime': '',  # sdk编译时间，实时时间，格式2020-07-29 20:23
                  'sdkName': '',
                  'sdkVersionName': '',
                  'headerRevisedVersion': '',  # sdk内header修订版本，header有改动则+1
                  },
        'X-Device-Info': {'model': '',  # 机型
                          'ht': '',  # 分辨率-高
                          'wd': '',  # 分辨率-宽
                          'brand': '',  # 品牌
                          'hardwareType': ''  # 设备类型：TV,Watch,Mobile(默认值)
                          },
        'X-Context': {'country': '',  # 设置国家
                      'timeZone': '',
                      'maskRegion': '',
                      'locale': ''
                      },
        'X-Sys': {'romVersion': '',
                  'osVersion': '',
                  'osVersionCode': '',
                  'osBuildTime': '',
                  'auid': '',
                  'ouid': '',
                  'duid': '',
                  'guid': '',
                  'apid': '',
                  'uid': '',
                  'usn': '',
                  'utype': '',
                  'betaEnv': ''
                  },
        'X-APP': {'appPackage': '支付测试demo',
                  'appVersion': '',
                  'deviceId': '',
                  'ucVersion': '',
                  'instantVersion': '',
                  'ucPackage': '',
                  'fromHT': '',
                  'registerId': '',
                  'overseaClient': '',
                  'payVersion': '',
                  'hostPackage': '',
                  'hostVersion': '',
                  'dynamicUIVersion2': ''
                  },
        'X-Safety': {'imei': '',
                     'hasPermission': '',
                     'imei1': '',
                     'mac': '',
                     'serialNum': '',
                     'deviceName': '',
                     'wifissid': '',
                     'slot0': '',
                     'slot1': ''
                     }
    }
    common_params = {
        'appKey': '',
        'sign': '',
        'timestamp': str(int(time.time() * 10**3)),
        'nonce': create_random_str(8)
    }
    resp_params = {'success': None, 'error': {'code': '', 'message': ''}, 'data': {}}

    def __init__(self, url_prefix=None, appkey='2033', **kwargs):
        """
        :param url_prefix: 域名
        :param partner_id: 业务线id
        :param kwargs: 请求参数
        """
        self.prefix = url_prefix if url_prefix else ''
        self.url = ''
        self.session = requests.Session()
        self.header = deepcopy(self.req_header)
        self.header.update(kwargs)
        self.__sessionKey = str_to_base64(create_random_str(16))
        print('X-Protocol sessionKey:', self.__sessionKey)
        iv4aes = create_random_str(16)
        self.__iv = str_to_base64(iv4aes).decode()
        print('X-Protocol iv:', self.__iv)
        self.__sessionTicket = None
        self.keys = Config(key_configfile_path).as_dict('encrypted_json')
        rsa_ = RSA(self.__sessionKey, encjson_rsa_public_key_path)
        self.__pub_sessionKey = rsa_.cipher()
        print('pub-sessionKey:', self.__pub_sessionKey)
        self.header['X-Protocol']['key'] = self.__pub_sessionKey
        self.header['X-Protocol']['iv'] = self.__iv
#         self.aes_codec = AES_CBC(self.__sessionKey.decode(), base64.b64decode(self.__iv))
        self.aes_codec = AES4J(self.__sessionKey.decode(), base64.b64decode(self.__iv),
                               self.header['X-Protocol-Ver'])
        self.common_params['appKey'] = appkey
        self.appSecret = Config(key_configfile_path).read_config('encrypted_json', 'app_secret')

    def post(self, url, data:dict):
        '''
        :param url:
        :param data: request parameters dict
        '''
        self.logger.info('原始header：%s', self.header)
        self.session.headers = self.encrypt_header()
        # self.logger.info('加密header：%s' % self.session.headers)
        self.url = self.prefix + url
        data.update(self.common_params)
        data['sign'] = self.make_sign(data)
        aes_body = self.encrypt_body(data)
        self.logger.info("url:%s" % self.url)
        self.logger.info("原始body:%s" % data)
        # self.logger.info("加密body:%s" % aes_body)
        try:
            response = self.session.post(url=self.url, data=aes_body)
            self.logger.info("返回状态码:{}".format(response.status_code))
            resp_text = self.aes_codec.decrypt(response.text)
            pyobj_resp = json.loads(resp_text, encoding='utf-8')
            self.logger.info("post返回：{}".format(pyobj_resp))
            # self.logger.info('POST返回结果:{}'.format(
            #     simplejson.dumps(pyobj_resp, ensure_ascii=False, encoding='utf-8', indent=2))
            # )
        except:
            raise HttpJsonException('<%s> exception: %s' % (type(self), sys.exc_info()[1]))
        else:
            self.logger.info('Response headers:%s', response.headers)
            self.__sessionTicket = response.headers['X-Session-Ticket']
            self.header['X-Protocol']['sessionTicket'] = self.__sessionTicket
            return pyobj_resp

    def make_sign(self, data: dict):
        '''
        第一步：对参数按照key=value的格式，并按照参数名ASCII字典序排序如下：
        stringA="param1=value1&param2=value2&nonce=100001&timestamp=1611647506";
        特别注意以下重要规则：
        ◆ 参数名ASCII码从小到大排序（字典序）；
        ◆ 如果参数的值为空不参与签名；
        ◆ 参数名区分大小写；
        ◆ 传送的sign参数不参与签名，将生成的签名与该sign值作校验。
        第二步：拼接API密钥
        stringSignTemp="stringA&key=192006250b4c09247ec02edce69f6a2d"
        sign=MD5(stringSignTemp)="9a0a8659f005d6984697e2ca0a9cf3b7"
        其中key的值为申请的appSecret，和appKey一起申请。
        '''
        orig_sign = Sign(data).join_asc_have_key('&key=' + self.appSecret)
        return md5(orig_sign, to_upper=False)

    def encrypt_header(self):
        to_bytes_keys = 'X-Protocol', 'X-SDK', 'X-Device-Info', 'X-Context', 'X-Sys', 'X-APP'
        enc_header = self.header.copy()
        '''urlencode 'X-Protocol', 'X-SDK', 'X-Device-Info', 'X-Context', 'X-Sys', 'X-APP'
        '''
        for k in to_bytes_keys:
            enc_header[k] = quote(str(enc_header[k]), encoding='utf-8')

        def encrypt_x_safety():
            '''
            1. aes_cbc encryption
            2. urlencode
            '''
            aes_x_safety = self.aes_codec.encrypt(str(enc_header['X-Safety']))
            urlencode_x_safety = quote(aes_x_safety, encoding='utf-8')
#             aes_x_safety = self.aes_codec.encrypt_and_base64(str(enc_header['X-Safety']))
#             _encoding = chardet.detect(aes_x_safety)['encoding']
#             urlencode_x_safety = quote(aes_x_safety.decode(_encoding), encoding='utf-8')
            return urlencode_x_safety

        enc_header['X-Safety'] = encrypt_x_safety()
        return enc_header

    def encrypt_body(self, body):
#         return self.aes_codec.encrypt_and_base64(str(body))
        return self.aes_codec.encrypt(str(body))
