'''
Created on 2021年8月30日
@author: 80319739
'''
import os
import random
from lib.common.session.http.http_json import HttpJsonSession
from lib.common.algorithm.md5 import md5
from lib.common_biz.sign import Sign
from lib.common.db_operation.mysql_operation import MySQLClient


if __name__ == '__main__':
#     httpjson = HttpJsonSession('https://jf-client-test.wanyol.com')     #credits-web测试1
    httpjson = HttpJsonSession('https://uc-credits-gateway-open.wanyol.com')    #credits-gateway-open测试1
#     app_packages = ('com.nearme.gamecenter.close', 'com.oppo.market', 'com.nearme.gamecenter.com', 'com.nearme.gamecenter', 
#                     'creditsmarket', 'com.oppo.integralshop', 'com.nearme.themespace'
#     )
#     app_pkg = random.choice(app_packages)
    mysql = MySQLClient('10.177.57.38', 'ucbaseuser', 'ucbaseuser', port=33066, db=None)
    mysql.logger.info('成功连接到测试环境1-MYSQL')
    req = {
        "ssoid": "2086776969",
        "country": "CN",
        "statusList": {
            "bizTaskId": "1",
            "updateTime": "1631783336201",
            "status": "ON"
        },
        "openId": "111111",
        "clientIp": "1.23.13.2",
        "sign": "",
        "appKey": "heytapvip",
        "iconUrl": "http://www.baidu.com/",
        "brand": "brand",
        "timestamp": "1631783336201"
    }
    result = mysql.select_one('SELECT app_key,app_secret FROM oppo_credits.credits_config_app WHERE app_key="%s"' %req['appKey'])
    app_secret = result['app_secret']
    temp_string = Sign(req).join_asc_have_key() + app_secret
    req['sign'] = md5(temp_string).lower()
    print(req)
    httpjson.post('/api/open/write/credits/third-task/push-status', data=req)
