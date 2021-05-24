# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/22 17:51
# comment:
import re
import json
import simplejson
import telnetlib
from lib.common.utils.meta import WithLogger
from six import with_metaclass
from lib.common.utils.misc_utils import ascii_to_chr_repr
from lib.common.utils.globals import MONITOR


class DubRunner(with_metaclass(WithLogger, telnetlib.Telnet)):
    prompt = 'dubbo>'
    coding = 'utf-8'

    def __init__(self, host=None, port=0):
        super().__init__(host, port)
        self.write(b'\n')
        self.errmsg = ''

    def command(self, flag, str_=""):
        data = self.read_until(flag.encode())
        self.write(str_.encode() + b"\n")
        return data

    def invoke(self, interface_name, method_name, arg, flag="JSON"):
        """
        :param interface_name:
        :param method_name:
        :param arg:
        :param flag: JSON传json；flag == "SINGLE_STRING",针对传单个字符串的情况；flag == "STRING"，针对传多个字符串的情况
        :return:
        """
        if flag == "JSON":
            command_str = "invoke {0}.{1}({2})".format(interface_name, method_name, arg)
            # 这个地方的arg不能写成json.dumps(arg)，即不能转换成string型，提高复用性，在调2个或2个以上的接口的方法的参数时
        elif flag == "SINGLE_STRING":
            str_arg = simplejson.dumps(arg, ensure_ascii=False)
            command_str = "invoke {0}.{1}('{2}')".format(interface_name, method_name, str_arg)
        elif flag == "STRING":
            command_str = "invoke {0}.{1}{2}".format(interface_name, method_name, arg)
        elif flag == "FIX":
            # 混合类型，直接传入字符串处理
            command_str = "invoke {0}.{1}({2})".format(interface_name, method_name, arg)
        self.command(DubRunner.prompt, command_str)
        # self.logger.info("dubbo传参：{}".format(simplejson.dumps(arg, ensure_ascii=False, indent=2)))
        self.logger.info("dubbo invoke语句：{}".format(command_str))
        data = self.command(DubRunner.prompt, "")
        resp = data.decode(encoding='utf-8', errors='ignore').split('elapsed')[0].strip('\n')
        self.logger.info('Dubbo Response: \n%s', resp)
        result = self.extract_result(resp)
        # 如果result为空，则用原始response
        to_be_processed = result or resp
        try:
            pyobj_result = json.loads(to_be_processed)
            return self.process_result(pyobj_result)
        except:
            # result不是字典
            return result
    
    def extract_result(self, resp):
        '''
        返回三种情况：        
        1. dubbo resp携带result后，正常返回result
        2. dubbo抛异常，返回异常
        3. 上述两者均不满足，则返回None
        :param resp: raw dubbo response
        '''
        try:
            result = re.search('result:\s*({.+})', resp, re.I).group(1)
            result = result.replace('\\', '').replace('"{', '{').replace('}"', '}')
            return result
        except AttributeError:
            try:
                self.errmsg = re.search('CommonSystemException: (.+)', resp, re.I).group(1)
            except:
                self.logger.debug("dubbo response doesn't have key `result`")
                return None
            else:
#                 raise AttributeError('Dubbo返回异常：'+errmsg)
                self.logger.error('Dubbo返回异常：'+self.errmsg)
                MONITOR.obj = self
                return self.errmsg
    
    def process_result(self, jsondata):
        authHint = jsondata.get('authHint')
        if isinstance(authHint, dict):
            mes = authHint.get('mes')
            if mes:
                authHint['mes'] = ascii_to_chr_repr(mes)
        elif authHint:
            authHint = ascii_to_chr_repr(authHint)
        self.logger.info("dubbo回参：{}".format(jsondata))
        return jsondata
    

if __name__ == '__main__':
    conn = DubRunner('10.3.1.79', 2181)
