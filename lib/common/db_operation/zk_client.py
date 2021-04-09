#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/4/7 10:40
# comment:
from kazoo.client import KazooClient
import urllib.parse
import re
from lib.common.utils.env import get_env_config, get_env_id
from lib.common.utils.meta import WithLogger


class ZkClient(metaclass=WithLogger):
    def __init__(self, ip, port=2181, time_out=100):
        self.ip = ip
        self.port = port
        self.time_out = time_out
        self.zk = KazooClient(hosts='{}:{}'.format(self.ip, self.port), timeout=self.time_out)
        self.zk.start()

    def get_node_info(self, service):
        # 获取dubbo节点下所有子节点
        node = self.zk.get_children('/dubbo')
        if service in node:
            providers = urllib.parse.unquote(self.zk.get_children("/dubbo/{}/providers".format(service))[0])
            self.logger.info("获取到具体的providers信息:{}".format(providers))
            ip_port_info = re.findall(r"dubbo://(.+?)/", providers)[0]
            ip_port = ip_port_info.split(":")
            interface_info = re.findall(r"interface=(.+?)&", providers)
            method_info = re.findall(r"methods=(.+?)&", providers)
            self.logger.info(service+"返回的端口和ip：{}".format(ip_port[0]))
            return {"ip_port": ip_port, "interface": interface_info, "method": method_info}
        else:
            self.logger.info("节点不存在")
        self.zk.stop()


def connect_zk(in_out='inland'):
    zk_info = get_env_config()['zk_' + in_out]
    zk_client = ZkClient(zk_info['host'], zk_info['port'])
    return zk_client


if __name__ == '__main__':
    a = connect_zk()
    b = a.get_node_info("com.oppo.zeus.mongo.order.service.QueryConsumeService")
    print(b)