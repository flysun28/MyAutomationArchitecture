#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/20 15:50
# comment:

import sys
import os
from .http_exception import *


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
        
        