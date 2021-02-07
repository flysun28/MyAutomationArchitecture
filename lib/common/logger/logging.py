#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:31
# comment:
import logging
import sys
import os
from datetime import date
from lib.config.path import log_dir


class Logger():
    logger_names = {}
    
    def __init__(self, name, console_stream=sys.__stderr__):
        """
        :param name: 日志打印名称
        :param path: 日志打印路径，默认为支付日志路径
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
#         self.logger.propagate = False
        # 日志分别打印在控制台以及写入日志文件
        # 文件写入debug及以上
        # 控制台只显示info及以上
        filename = 'securepayment_lib-' + str(date.today())
        log_path = os.path.join(log_dir, filename)
        file_hdlr = logging.FileHandler(log_path, encoding='utf-8')
        file_hdlr.setLevel(logging.DEBUG)
        console_hdlr = logging.StreamHandler(console_stream)
        console_hdlr.setLevel(logging.INFO)
        # 设置日志格式，并应用到file和console中
#         formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(module)s-%(lineno)s: %(message)s')
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(name)s-%(lineno)s-%(message)s')
        file_hdlr.setFormatter(formatter)
        console_hdlr.setFormatter(formatter)
        self.logger.addHandler(file_hdlr)
        self.logger.addHandler(console_hdlr)
        self.register()

    def get_logger(self):
        return self.logger_names.get(self.logger.name, self.logger)
    
    def register(self):
        self.logger_names.setdefault(self.logger.name, self.logger)

    
    
