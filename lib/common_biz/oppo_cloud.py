'''
Created on 2021年3月31日
@author: 80319739
'''
import time
import requests
from lib.common_biz.sign import Sign
from lib.common.algorithm.md5 import md5
from lib.common.session.http.http_json import HttpJsonSession
from lib.common.utils.env import get_env_id

test_http_ui = 'http://10.176.253.176:8099/swagger/index.html'


class HttpOPPOCloud(HttpJsonSession):
    psa_name_to_id = {'fspay': '50280'}
    product_domain = 'http://prod-console.cloud.oppoer.me'
    test_domain = ''
    '''
    刘成(W9007972) 申请的appkey+secret
    '''
    def __init__(self, **kwargs):
#         self.prefix = self.test_domain if get_env_id().isdigit() else self.product_domain
        self.prefix = self.product_domain
        super().__init__(url_prefix=self.prefix, **kwargs)

    def get_sla_interface(self, psa, is_dash=True):
        req = {
            'appKey': 'slainterface',
            'ts': int(time.time() * 10**3),
            'sign': '',
            'psaId': self.psa_name_to_id[psa],
            'isDash': '1' if is_dash else '0'
        }
        orig_sign_str = Sign(req).join_asc_have_key('&appSecret=') + '7cdb3bf0150c4fbf9a29df17b9eeda4a'
        req['sign'] = md5(orig_sign_str, to_upper=False)
        suffix = '&'.join(['{}={}'.format(k, v) for k, v in req.items()])
        result = self.get('/monitor_api/sla/sla/interface?' + suffix)
        return [d['path'] for d in result['data'][0]['items']]


if __name__ == '__main__':
    oppo_cloud = HttpOPPOCloud()
    print(oppo_cloud.get_sla_interface('fspay', is_dash=True))