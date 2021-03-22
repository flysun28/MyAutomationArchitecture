# coding=utf-8
'''
@author: 80319739
'''
import http
from requests.exceptions import *


class HttpJsonException(Exception):
    
    def __str__(self, *args):
        largs = list(args)
        for idx, arg in enumerate(largs):
            if type(arg) is RequestException or arg.__base__ is RequestException:
                largs[idx] = str(arg)
        args = ['<HttpJson> exception:'] + largs
        return ' '.join(args)

