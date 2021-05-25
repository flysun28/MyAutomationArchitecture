# coding=utf-8
'''
@author: 80319739
'''
import http
from requests.exceptions import *


class HttpJsonException(Exception):
    
    def __str__(self):
        largs = list(self.args)
        for idx, arg in enumerate(self.args):            
            if getattr(type(arg), '__base__', None):  # arg is an instance object                
                if type(arg) is RequestException or type(arg).__base__ is RequestException:                    
                    largs[idx] = str(arg)        
        if '%' in largs[0]:
            msg = largs[0] %tuple(largs[1:])
        else:            
            msg = ' '.join(largs)
        args = '<HttpJson> exception:' + msg
        return args


class LoginError(Exception):
    pass
        