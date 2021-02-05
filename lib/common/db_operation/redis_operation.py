#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 22:58
# comment: redis操作
import sys
from common.utils.meta import WithLogger
try:
    from rediscluster import StrictRedisCluster
except ImportError:
    from rediscluster import RedisCluster
finally:
    this_mod = sys.modules.get(__name__, None)
    RedisClusterCls = getattr(this_mod, 'StrictRedisCluster', None) or getattr(this_mod, 'RedisCluster', None)
#     print(sys.modules[RedisClusterCls.__module__].__file__)
from common.utils.env import get_env_config


class RedisCluster(metaclass=WithLogger):
    
    def __init__(self, conn_list):
        self.conn_list = conn_list  # 连接列表
        self.redis_conn = None

    def connect(self):
        """
        连接redis集群
        :return: object
        """
        try:
            # 非密码连接redis集群
            self.redis_conn = RedisClusterCls(startup_nodes=self.conn_list, decode_responses=True)
            self.logger.info("连接redis集群{}成功".format(self.conn_list))
            # 使用密码连接redis集群
            # redis_conn = StrictRedisCluster(startup_nodes=self.conn_list, password='123456')            
        except Exception as e:
            self.logger.logger(e)
            self.logger.info("连接redis集群{}失败".format(self.conn_list))
        print(self.redis_conn)

    def get_state(self):
        """
        获取状态
        :return:
        """        
        # print("连接集群对象",res,type(res),res.__dict__)
        if not self.redis_conn:
            return False
        dic = self.redis_conn.cluster_info()  # 查看info信息, 返回dict
        for i in dic:  # 遍历dict
            ip = i.split(":")[0]
            if dic[i].get('cluster_state'):  # 获取状态
                self.logger.info("节点状态, ip: %s\tvalue: %s" %(ip, dic[i].get('cluster_state')))


def connect_redis():
    """
    redis连接
    :return:
    """
    redis_args = get_env_config()['redis']
    # 存放集群信息
    conn_list = []
    hosts = redis_args['host'].replace(' ', '').split(',')
    ports = redis_args['port'].replace(' ', '').split(',')
    if len(ports) == 1:
        ports *= len(hosts)    
    for (host, port) in zip(hosts, ports):
        conn_list.append({'host': host, 'port': port})
    
    # 连接集群
    redis = RedisCluster(conn_list)
    redis.connect()
    redis.logger.info('connection list: %s', conn_list)
    return redis.redis_conn


