# coding=utf-8

import sys
import re
from lib.common.logger.logging import Logger
from abc import ABCMeta
from lib.common.concurrent.threading import monitor
# from lib.common.concurrent.threading import ExceptionMonitorThread


class WithLogger(ABCMeta):
    
    def __call__(cls, *args, **kwargs):        
        '''
        1. 生成cls.logger
        2. 判断cls是否为单例
        3. 生成实例
        4. 判断cls或实例是否需要监控异常
        '''
        module = sys.modules[cls.__module__]
        if cls.__module__ == '__main__':
            module_name = re.search('(securepayments|)(_|)lib(\S+).py', module.__file__, re.I).group(2)
            module_name = module_name.strip('\\').replace('\\', '.')
        else:
            module_name = module.__name__
        logger = getattr(module, 'logger', None)
        if logger:
            cls.logger = logger
        else:
            module.logger = cls.logger = Logger(module_name, sys.__stdout__).get_logger()
        
        def instantiating():
            self = type.__call__(cls, *args, **kwargs)
            # cls.monitored，当类被monitoring装饰后
            monitored = getattr(cls, 'monitored', None)
            if monitored is True:
                monitor.obj2exc.setdefault(self, '')
            return self
        
        # 判断是否单例
        for k, v in cls.__dict__.items():
            if re.search('single', k, re.I):
                is_singleton = v
                break
        else:
            is_singleton = False
        if is_singleton:
            instance = getattr(cls, 'instance', None)
            if instance is None:
                # 实例化
                cls.instance = instantiating()
            return cls.instance
        else:
            # 实例化
            return instantiating()


__builtins__.update(WithLogger=WithLogger)
