#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/20 15:50
# comment:

import sys
import os
import time
from _functools import partial
from .http_exception import *
from .intf_exception import *



class _Anonymous(): pass

this_module = sys.modules[_Anonymous.__module__]
this_package = sys.modules[this_module.__package__]


# def import_package_all_classes(root_dir):
#     for root, dirnames, filenames in os.walk(root_dir):
#         print(root, dirnames, filenames)        
#         [dirnames.remove(dirname) for dirname in dirnames.copy() if dirname.startswith('_')]
#         py_modnames = [filename for filename in filenames if os.path.splitext(filename)[1] == '.py']
#         for dirname in dirnames:
#             subdir = os.path.join(root, dirname)
#             import_modules_recursively(subdir)
#         for modname in py_modnames:
#             exec('from .{} import *'.format(modname))
#             qual_modname = os.path.join(root, modname)
#             sys.modules[qual_modname] = 0


# import_modules_recursively(pardir(__file__))


class WaitUntilTimeOut(metaclass=WithLogger):
    
    def __init__(self, true_condition:str, timeout=10, interval=1):
        assert isinstance(true_condition, str), '`true_condition` must be a string'
        self.condition = true_condition
        self.timeout = timeout
        self.interval = interval
    
    def __enter__(self):
#         self.wait()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if any([exc_type, exc_val, exc_tb]):
            self.logger.error(exc_val)
    
    def wait(self):
        start = time.perf_counter()
        while time.perf_counter() - start < self.timeout:
            if eval(self.condition):
                break
            else:
                time.sleep(self.interval)
        else:
            raise TimeoutError('Exceed %d, timeout occurred!!!' %self.timeout)
    
            