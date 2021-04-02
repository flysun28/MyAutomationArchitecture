'''
Created on 2021年4月2日
@author: 80319739
'''
import pytest
from lib.common.session.http.http_json import EncryptJson
from lib.common.utils.globals import GlobalVar

pytestmark = pytest.mark.pb2json


@pytest.fixture(scope='module', autouse=True)
def encjson():
    yield EncryptJson(GlobalVar.URL_PAY_IN, appkey='2033')
    

def test_service_info(encjson):
    encjson.header['X-Context']['country'] = 'CN'
    encjson.header['X-Device-Info']['brand'] = 'OPPO'
    result = encjson.post('/api/conf/v1/service-base-info', {'partnerId': '2031'})
    print(result['data']['contactInfo'])


def test_wallet_package(encjson):
    result = encjson.post('/api/conf/v1/package-name', {})
    print(result['data']['walletPackageName'])
    