# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/22 17:51
# comment:
import json
import telnetlib
import socket
from lib.common.logger.logging import Logger
logger = Logger("DubRunner").get_logger()


class DubRunner(telnetlib.Telnet):
    prompt = 'dubbo>'
    coding = 'utf-8'

    def __init__(self, host=None, port=0, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
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
            command_str = "invoke {0}.{1}('{2}')".format(
                service_name, method_name, arg)
        elif flag == "STRING":
            command_str = "invoke {0}.{1}{2}".format(
                service_name, method_name, arg)
        self.command(DubRunner.prompt, command_str)
        logger.info("dubbo传参：{}".format(command_str))
        data = self.command(DubRunner.prompt, "")
        # data = data.decode(DubRunner.coding, errors='ignore').split('\n')[0].strip()
        temp = str(data, encoding="gbk").split("elapsed")[0]
        data = json.loads(temp)
        logger.info("dubbo回参：{}".format(data))
        return data


if __name__ == '__main__':
    conn = DubRunner('10.3.1.79', 2181)
