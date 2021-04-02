#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 22:58
# comment: xml操作
import re
from lxml import etree
from lib.common.utils.meta import WithLogger
from lib.common.file_operation.config_operation import Config
from lib.config.path import maven_cfg_path


class XML(metaclass=WithLogger):
    
    def __init__(self, src_path):
        self.path = src_path
        self.root = etree.parse(src_path).getroot()
        self._ns = None
        self.namespace = None
    
    def __iter__(self):
        is_finished = yield from self._yield()
        print('Iterate %s finished? %s' %(self.path, is_finished))

    def _yield(self, root=None):
        root = self.root if root is None else root
        for child in root:
            if type(child) is etree._Element:
                if child.getchildren():
                    yield from self._yield(child)
                else:
                    yield child
        return True
            
    def show_value(self, tag):
        for child in self:
#             print(child, child.tag, child.text)
            if re.search('\{%s\}%s' %(self.namespace, tag), str(child.tag), re.I):
                return child.text
    
    def traverse(self):
        return list(self)
            

class MvnSettingXML(XML):
    
    def __init__(self):
        src_path = Config(maven_cfg_path).read_config('settings', 'path')
        super().__init__(src_path)
        self._repo = None
        self.local_repo = 'localRepository'

    @property
    def namespace(self):
        return self._ns
    
    @namespace.setter
    def namespace(self, _):
        for ns in self.root.nsmap.values():
            if ns in self.root.tag:
                self._ns = ns
                break
        else:
            self.logger.info(self.root.tag, self.root.nsmap)
            raise LookupError('<class MvnSettingXML> %s: get namespace failed' %self.path)
    
    @property
    def local_repo(self):
        return self._repo
    
    @local_repo.setter
    def local_repo(self, tag):
        self._repo = self.show_value(tag)


