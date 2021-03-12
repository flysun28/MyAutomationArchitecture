#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 22:57
# comment:

import pymysql
from lib.common.utils.meta import WithLogger
from lib.common.utils.env import get_env_config, get_env_id
from lib.common.logger.logging import Logger


class MySQLClient(metaclass=WithLogger):
# class MySQLClient():
#     logger = Logger('MYSQL操作').get_logger()
    def __init__(self, host, user, pwd, port=3306, db=None): 
        port = int(port)
        self.attrs = {}
        self.attrs.update(host=host, user=user, password=pwd, port=port, db=db)
        # 创建连接
        self.conn = pymysql.connect(host=host, user=user, password=pwd, port=port, charset='utf8', db=db)
        self.conn.autocommit(True)
        # 创建游标，字典形式返回
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)
        
    def __enter__(self):
        self.logger.info('Connect to mysql: <%s>' % self.attrs)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出时关闭游标关闭连接"""
        self.cur.close()
        self.conn.close()
        
    def select(self, sql):
        """查询数据"""
        self.logger.info('执行sql语句：{}'.format(sql))
        self.cur.execute(sql)  # 查询数据
        res = self.cur.fetchall()
        for one in res:
            for k, v in one.items():
                one[k] = '' if v is None else v
        self.logger.info('查询结果：%s', res)
#         [{k:('' if v is None else v) for one in res for k, v in one.items()}]
        return res

    def select_one(self, sql):
        """
        查询一条数据
        :param sql:
        :return:
        """
        self.logger.info('执行sql语句：{}'.format(sql))
        self.cur.execute(sql)  # 查询数据
        res = self.cur.fetchone()
        for k, v in res.items():
            res[k] = '' if v is None else v
        if res is None:
            self.logger.info('查询数据为空')
        return res

    def execute(self, sql):
        """执行sql"""
        try:
            # 执行SQL语句
            self.cur.execute(sql)
            self.logger.info("执行sql语句：{}".format(sql))
            # 提交事务到数据库执行
            self.conn.commit()  # 事务是访问和更新数据库的一个程序执行单元
        except BaseException as f:
            self.logger.info(f)
            self.conn.rollback()
#             raise
        # 返回受影响行数
        return self.cur.rowcount

    def executemany(self, sql, params):
        """
        批量插入数据
        :param sql:    插入数据模版, 需要指定列和可替换字符串个数
        :param params:  插入所需数据，列表嵌套元组[(1, '张三', '男'),(2, '李四', '女'),]
        :return:    影响行数
        """
        try:
            # sql = "INSERT INTO USER VALUES (%s,%s,%s,%s)"  # insert 模版
            # params = [(2, 'fighter01', 'admin', 'sanpang'),
            #           (3, 'fighter02', 'admin', 'sanpang')]  # insert数据，
            self.cur.executemany(sql, params)
            self.conn.commit()
        except BaseException as f:
            self.logger.info(f)
            self.conn.rollback()
        return self.cur.rowcount
    

def connect_mysql(in_out='inland', database=None):
    """
    连接mysql或指定数据库,注意配置文件的顺序（用户名，密码，端口、地址）    
    :param in_out: inland, oversea
    :param database:
    :return:
    """
    if is_connect_mysql():
        mysql_args = get_env_config()['mysql_'+in_out]
        if database:
            mysql_args.update(db=database)
        mysql = MySQLClient(**mysql_args)
        mysql.logger.info('成功连接到测试环境%s-MYSQL：%s' % (get_env_id(), mysql_args))
        return mysql
    else:
        return None


def connect_auto_test_special(database=None):
    """
    连接自动化测试专用数据库
    :param database:
    :return:
    """
    mysql_args = {'host': '10.52.54.122',
                  'user': 'opay',
                  'pwd': '_UI7xHubrhTPIP1J_T4so7SU7ATCrUzm7cAh6TdBLLHWUSQUQqD8p45xVQzV3Czi',
                  'port': '33066'}
    if database:
        mysql_args.update(db=database)
    mysql = MySQLClient(**mysql_args)
    mysql.logger.info('成功连接到测试专用环境-MYSQL：%s' % mysql_args)
    return mysql


def is_connect_mysql():
    """
    是否连接数据库标识
    :param env:
    :return:
    """
    env = get_env_id()
    if env == "1" or env == "2" or env == "3":
        return True
    elif env == "grey" or env == "product":
        return False


if __name__ == '__main__':
    print(connect_mysql("", ""))