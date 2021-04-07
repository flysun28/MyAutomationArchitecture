# coding=utf-8

import sys
import re
from lib.common.logger.logging import Logger
from abc import ABCMeta


class WithLogger(ABCMeta):
    
    def __call__(cls, *args, **kwargs):
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
        return type.__call__(cls, *args, **kwargs)
    

__builtins__.update(WithLogger=WithLogger)
