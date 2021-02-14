# coding=utf-8
'''
@author: 80319739
'''
import http
from requests.exceptions import *


class HttpJsonException(Exception):
    
    def __str__(self, *args):
        for arg in args:
            if type(arg) is RequestException or arg.__base__ is RequestException:
                arg = str(arg)
        args = ('<HttpJson> exception:', ) + args
        return ' '.join(args)

