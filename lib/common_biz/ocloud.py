'''
Created on 2021年7月23日
@author: 80319739
@description: 云服务接口
'''
import requests
import time
from lib.common.utils.globals import GlobalVar
import simplejson


class Ocloud():
    
    def __init__(self):
        '''
        云服务测试环境域名: "http://album.ocloud-zx.ocloud-test.wanyol.com/pay"
        '''
        self.prefix = 'http://album.ocloud-zx.ocloud-test.wanyol.com/pay'

    def update_expire_time(self):
        '''
        设置当前生效套餐的过期时间为当前时间
        hash值：
        海外 ssuupv80105841andoppo18576683209ouwejksfjou
        国内 ssuupv80105841andoppo18576683209OnlyUsedForTest
        '''
        url = self.prefix + "/order/v1/orderUpdateOnlyUsedForTest?expireTimeStr={}".format(int(time.time())) + \
                "&hash=ssuupv80105841andoppo18576683209OnlyUsedForTest"
        header = {"OCLOUD-IMEI": '868631049869970', "OCLOUD-TOKEN": GlobalVar.TOKEN}
        print("url:", url)
        print("header:", header)
        resp = requests.get(url=url, headers=header)
        print(simplejson.dumps(resp.json(), ensure_ascii=False, indent=2))
