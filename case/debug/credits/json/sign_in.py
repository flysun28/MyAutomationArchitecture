'''
Created on 2021年8月30日
@author: 80319739
'''
import jnius_config
import os
import random
from lib.common.session.http.http_json import HttpJsonSession
from lib.common.algorithm.md5 import md5
from lib.common_biz.sign import Sign
from lib.config.path import case_dir
from lib.common.exception.intf_exception import IgnoreException
from lib.common.db_operation.mysql_operation import MySQLClient


def get_java_class(jar_name, clspath:str):
    jar_dir = os.path.join(case_dir, 'src', 'jar')
    with IgnoreException(jnius_config.set_classpath, '.', os.path.join(jar_dir, jar_name)) as _:
        '''
        autoclass必须在set_classpath之后导入，否则会报VM is already running, can't set classpath/options
        '''
        from jnius import autoclass
        return autoclass(clspath)


if __name__ == '__main__':
    httpjson = HttpJsonSession('https://jf-client-test.wanyol.com') #积分测试1
    app_packages = ('com.nearme.gamecenter.close', 'com.oppo.market', 'com.nearme.gamecenter.com', 'com.nearme.gamecenter', 
                    'creditsmarket', 'com.oppo.integralshop', 'com.nearme.themespace'
    )
    app_pkg = random.choice(app_packages)
    mysql = MySQLClient('10.177.57.38', 'ucbaseuser', 'ucbaseuser', port=33066, db=None)
    mysql.logger.info('成功连接到测试环境1-MYSQL')
    result = mysql.select_one('SELECT app_key,package,app_secret FROM oppo_credits.credits_config_app WHERE package="%s"' %app_pkg)
    app_secret = result['app_secret']
    '''
    # 已能定位到class，但识别导入其他依赖库失败，目前无法解决
    jcls = get_java_class('atms-customize.jar', 'src.main.java.com.oppo.itest.stp.customize.LazyFunction')
    print(jcls)
    '''
    req = {
        "ssoid": "2086776969",
        "appPackage": app_pkg,
        "country": "CN",
        "providerResult": "",
        "clientIp": "1.2.3.4",
        "sign": "",
        "imei": "2",
        "actionId": "",
        "processToken": '',   # jcls.generateProcessToken('2086776969', app_pkg),
        "model": "1",
        "token": "TOKEN_7t5kusT0owaYVytvYSs24GzZ3PY7O7hMevBOFXsgEWzD/Fhr6DDJ+oh5lgZHhNtr",
        "timestamp": "1631157714935"
    }
    temp_string = Sign(req).join_asc_have_key() + app_secret
    req['sign'] = md5(temp_string)
    print(req)
    httpjson.post('/route/v3/sign', data=req)
