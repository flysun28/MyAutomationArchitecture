# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/22 17:51
# comment:
import json
import simplejson
import telnetlib
import socket
from lib.common.utils.meta import WithLogger
from six import with_metaclass


class DubRunner(with_metaclass(WithLogger, telnetlib.Telnet)):
    prompt = 'dubbo>'
    coding = 'utf-8'

    def __init__(self, host=None, port=0):
        super().__init__(host, port)
        self.write(b'\n')

    def command(self, flag, str_=""):
        data = self.read_until(flag.encode())
        self.write(str_.encode() + b"\n")
        return data

    def invoke(self, service_name, method_name, arg, flag="JSON"):
        """
        :param service_name:
        :param method_name:
        :param arg:
        :param flag: JSON传json；flag == "SINGLE_STRING",针对传单个字符串的情况；flag == "STRING"，针对传多个字符串的情况
        :return:
        """
        if flag == "JSON":
            command_str = "invoke {0}.{1}({2})".format(
                service_name, method_name, arg)
            # 这个地方的arg不能写成json.dumps(arg)，即不能转换成string型，提高复用性，在调2个或2个以上的接口的方法的参数时
        elif flag == "SINGLE_STRING":
            str_arg = simplejson.dumps(arg, ensure_ascii=False)
            command_str = "invoke {0}.{1}('{2}')".format(
                service_name, method_name, str_arg)
        elif flag == "STRING":
            command_str = "invoke {0}.{1}{2}".format(
                service_name, method_name, arg)
        elif flag == "FIX":
            # 混合类型，直接传入字符串处理
            command_str = "invoke {0}.{1}({2})".format(
                service_name, method_name, arg)
        self.command(DubRunner.prompt, command_str)
        # self.logger.info("dubbo传参：{}".format(simplejson.dumps(arg, ensure_ascii=False, indent=2)))
        self.logger.info("dubbo invoke语句：{}".format(command_str))
        data = self.command(DubRunner.prompt, "")
        # data = data.decode(DubRunner.coding, errors='ignore').split('\n')[0].strip()
        resp = data.decode(encoding='gbk', errors='ignore').split('elapsed')[0]
#         print(resp)
        data = json.loads(resp)
        self.logger.info("dubbo回参：{}".format(data))
        return data


if __name__ == '__main__':
    conn = DubRunner('10.3.1.79', 2181)
