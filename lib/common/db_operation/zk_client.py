# -*- encoding:utf-8 *-*
# author:yf
# datetime:2021/4/7 10:40
# comment:
import kazoo
import urllib
import re
from lib.common.utils.meta import WithLogger
from six import with_metaclass
from kazoo.handlers.threading import SequentialThreadingHandler

class SequentialThreadingHandlerExt(with_metaclass(WithLogger, SequentialThreadingHandler)):
    def _create_thread_worker(self, queue):
        def _thread_worker():  # pragma: nocover
            while True:
                try:
                    func = queue.get()
                    try:
                        if func is object():
                            break
                        func()
                    except TypeError:
                        continue
                    except Exception:
                        self.logger.exception("Exception in worker queue thread")
                    finally:
                        queue.task_done()
                        del func  # release before possible idle
                except (self.queue_empty, RuntimeError):
                    continue
        type(self)._thread_worker = _thread_worker
        t = self.spawn(type(self)._thread_worker)
        return t

kazoo.handlers.threading.SequentialThreadingHandler = SequentialThreadingHandlerExt
 
from kazoo.client import KazooClient
from lib.common.utils.env import get_env_config


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
            if self.zk.get_children("/dubbo/{}/providers".format(service)):
                providers = urllib.parse.unquote(self.zk.get_children("/dubbo/{}/providers".format(service))[0])
                self.logger.info("获取到具体的providers信息:{}".format(providers))
                ip_port_info = re.findall(r"dubbo://(.+?)/", providers)[0]
                ip_port = ip_port_info.split(":")
                interface_info = re.findall(r"interface=(.+?)&", providers)
                method_info = re.findall(r"methods=(.+?)&", providers)
                self.logger.info(service + "的IP和端口:  {}:{}".format(*ip_port))
                return {"ip_port": ip_port, "interface": interface_info, "method": method_info}
            else:
                self.logger.info("providers为空")
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