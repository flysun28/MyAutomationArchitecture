# coding=utf-8

import http
from requests.exceptions import *


class HttpJsonException(Exception):
    
    def __str__(self, *args):
        for arg in args:
            if type(arg) is RequestException:
                arg = str(arg)
        args = ('<HttpJson> exception:', ) + args
        return ' '.join(args)

