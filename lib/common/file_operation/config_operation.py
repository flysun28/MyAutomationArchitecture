#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 22:57
# comment: 配置文件操作

import configparser
import json
from lib.common.utils.meta import WithLogger


class Config(metaclass=WithLogger):
    
    def __init__(self, path):
        """
        :param path: 配置文件配置路径
        """
        self.path = path
        self.parser = configparser.ConfigParser()

    def write_config(self, section, option, value):
        """
        :param option:
        :param section:
        :param value: 写入的值
        :return:
        """        
        self.parser.read(self.path, encoding='utf-8')
        self.parser.set(section, option, str(value))
        with open(self.path, 'w', encoding='utf-8') as f:
            self.parser.write(f)

    def read_config(self, section, option):
        """
        读配置文件
        :param section:
        :param option:
        :return:
        """        
        self.parser.read(self.path)
        try:
            option_value = self.parser.get(section, option)
            return option_value
        except Exception as e:
            self.logger.info('配置文件%s未配置执行用例或配置错误' %self.path)

    def sections(self)-> list:
        """
        获取所有的sections
        :return:
        """        
        self.parser.read(self.path)
        return self.parser.sections()

    def options(self, section) -> list:
        """
        获取options
        :param section:
        :return:
        """        
        self.parser.read(self.path)
        return self.parser.options(section)
    
    def as_dict(self, section, *options):
        result = {}
        if not options:
            options = self.options(section)
        for option in options:
            result.setdefault(option, self.read_config(section, option))
        return result

    def value_as_list(self, section, option):
        """
        陪自己文件读取都以str返回，使用json.loads转换过程list，dict等数据类型
        :param section:
        :param option:
        :return:
        """
        return json.loads(Config(self.path).read_config(section, option))


if __name__ == '__main__':
    from lib.common_biz.file_path import join_sign_path
    a = Config(join_sign_path).sections()
    print(a)