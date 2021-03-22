#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/22 19:11
# comment:
import requests
import json
import time
import chardet
from requests.exceptions import RequestException
from lib.common.utils.meta import WithLogger
from lib.common.exception import HttpJsonException
from lib.common_biz.sign import Sign
from lib.common.utils.misc_utils import create_random_str
from lib.common.file_operation.config_operation import Config
from lib.config.path import key_configfile_path
from lib.common.algorithm.aes import AES_CBC
from lib.common.algorithm.other import str_to_base64
from lib.common.algorithm.cipher import RSA
from lib.common_biz.file_path import encjson_rsa_public_key_path
from lib.common.algorithm.md5 import md5
from urllib.parse import quote


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
            self.logger.info(self.url)
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


class EncryptJson(HttpJsonSession):
    req_header = {
        'Content-Type': 'application/encrypted-json;charset=utf-8',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'User-Agent': 'EncryptJson/1.0',
        'X-Protocol-Ver': '3.0',
        'X-Protocol': {'key': '',     #RSA公钥加密后的sessionKey
                       'iv': '',      #key对应的随机iv信息
                       #会话秘钥，服务端用对称私钥加密sessionKey后的产物，由服务端回传给客户端，下一次通讯用该字段代替sessionKey
                       'sessionTicket': ''    
                      },
        'X-SDK': {'sdkBuildTime': '', #sdk编译时间，实时时间，格式2020-07-29 20:23
                  'sdkName': '',
                  'sdkVersionName': '',
                  'headerRevisedVersion': '',  #sdk内header修订版本，header有改动则+1
                 },
        'X-Device-Info': {'model': '',    #机型
                          'ht': '',    #分辨率-高
                          'wd': '',    #分辨率-宽
                          'brand': '',    #品牌
                          'hardwareType': ''  #设备类型：TV,Watch,Mobile(默认值)
                         },
        'X-Context': {'country': '',   #设置国家
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
        'X-APP': {'appPackage': '',
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

    def __init__(self, url_prefix=None, partner_id='2033', **kwargs):
        """
        :param url_prefix: 域名
        :param partner_id: 业务线id
        :param kwargs: 请求参数
        """
        self.prefix = url_prefix if url_prefix else ''
        self.url = ''
        self.session = requests.Session()
        self.req_header.update(kwargs)
        self.__sessionKey = str_to_base64(create_random_str(16))
        print('sessionKey:', self.__sessionKey)
        iv4aes = create_random_str(16).encode('utf-8')
        self.__iv = str_to_base64(iv4aes.decode('utf-8')).decode()
        self.__sessionTicket = None
        self.keys = Config(key_configfile_path).as_dict('encrypted_json')        
        rsa_ = RSA(self.__sessionKey, encjson_rsa_public_key_path)
        self.__pub_sessionKey = rsa_.cipher()
        print('pub-sessionKey:', self.__pub_sessionKey)      
        self.req_header['X-Protocol']['key'] = self.__pub_sessionKey
        self.req_header['X-Protocol']['iv'] = self.__iv
        self.aes_cbc = AES_CBC(self.__sessionKey, iv4aes)
        self.common_params['appKey'] = partner_id
        self.logger.info('原始header：%s', self.req_header)
        self.session.headers = self.encrypt_header()
    
    def post(self, url, data:dict):
        '''
        :param url:
        :param data: request parameters dict
        '''
        self.url = self.prefix + url
        data.update(self.common_params)
        data['sign'] = self.make_sign(data)
        aes_body = self.encrypt_body(data)
        self.logger.info("url:%s" %self.url)
        self.logger.info("原始body:%s" %data)
        self.logger.info("加密body:%s" %aes_body)
        try:
            response = self.session.post(url=self.url, data=aes_body)
#             print(response.content)
            self.logger.info("返回状态码:{}".format(response.status_code))
            self.logger.info('POST返回结果:{}'.format(response.json()))
        except:
            raise
        else:
            resp_json = response.json()
            print('Response headers:', response.headers)
            self.__sessionTicket = response.headers['X-Session-Ticket']
            return resp_json
    
    def make_sign(self, data:dict):
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
        orig_sign = Sign(data).join_asc_have_key('key='+self.keys['salt_key'])
        return md5(orig_sign, to_upper=False)
        
    def encrypt_header(self):
        to_bytes_keys = 'X-Protocol', 'X-SDK', 'X-Device-Info', 'X-Context', 'X-Sys', 'X-APP'
        enc_header = self.req_header.copy()
        '''urlencode 'X-Protocol', 'X-SDK', 'X-Device-Info', 'X-Context', 'X-Sys', 'X-APP'
        '''
        for k in to_bytes_keys:
            enc_header[k] = quote(str(enc_header[k]), encoding='utf-8')

        def encrypt_x_safety():
            '''
            1. aes_cbc encryption
            2. urlencode
            '''
            aes_x_safety = self.aes_cbc.encrypt_and_base64(str(enc_header['X-Safety']))
            print(aes_x_safety)
            urlencode_x_safety = quote(aes_x_safety.decode(chardet.detect(aes_x_safety)['encoding']),
                                       encoding='utf-8')
            return urlencode_x_safety
        
        enc_header['X-Safety'] = encrypt_x_safety()
        self.logger.info('加密header：%s' %enc_header)
        return enc_header
    
    def encrypt_body(self, body):
        enc_body = self.aes_cbc.encrypt_and_base64(str(body))
        return enc_body
