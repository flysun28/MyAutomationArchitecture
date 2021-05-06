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
    
    def __init__(self, name, console_stream=sys.__stdout__):
        """
        :param name: 日志打印名称
        :param console_stream: 日志输出流文件，默认为标准输出，可以修改为sys.__stderr__
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
#         self.logger.propagate = False
        # 日志分别打印在控制台以及写入日志文件
        # 文件写入debug及以上
        # 控制台只显示info及以上
        filename = 'securepayment_lib-{}.log'.format(str(date.today()))
        log_path = os.path.join(log_dir, filename)
        file_hdlr = logging.FileHandler(log_path, mode='a+', encoding='utf-8')
        file_hdlr.setLevel(logging.DEBUG)
        console_hdlr = logging.StreamHandler(console_stream)
        console_hdlr.setLevel(logging.INFO)
        # 过滤器：限制warning以下等级为标准输出打印
        console_filter = logging.Filter(name)
        console_filter.filter = lambda record: record.levelno < logging.WARNING
        console_hdlr.addFilter(console_filter)
        # warning及以上等级设置为标准错误打印
        error_hdlr = logging._StderrHandler(level=logging.WARNING)
        # 设置日志格式，并应用到file和console中
#         formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(module)s-%(lineno)s: %(message)s')
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(name)s-%(lineno)s-%(message)s')
        file_hdlr.setFormatter(formatter)
        console_hdlr.setFormatter(formatter)
        error_hdlr.setFormatter(formatter)
        self.logger.addHandler(file_hdlr)
        self.logger.addHandler(console_hdlr)
        self.logger.addHandler(error_hdlr)
        self.register()

    def get_logger(self):
        return self.logger_names.get(self.logger.name, self.logger)
    
    def register(self):
        self.logger_names.setdefault(self.logger.name, self.logger)

    

