'''
Created on 2021年4月2日
@author: 80319739
'''
import pytest
from lib.common.utils.globals import HTTPENCJSON_IN


pytestmark = pytest.mark.pb2json


def test_service_info():
    HTTPENCJSON_IN.header['X-Context']['country'] = 'CN'
    HTTPENCJSON_IN.header['X-Device-Info']['brand'] = 'OPPO'
    result = HTTPENCJSON_IN.post('/api/conf/v1/service-base-info', {'partnerId': '2031'})
    print(result['data']['contactInfo'])


def test_wallet_package():
    result = HTTPENCJSON_IN.post('/api/conf/v1/package-name', {})
    pkg_name = result['data']['walletPackageName']
    print('钱包包名:', pkg_name)
    assert pkg_name == 'com.finshell.wallet', pkg_name