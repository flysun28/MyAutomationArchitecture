# coding=utf-8
import sys
import traceback
from lib.common.utils.meta import WithLogger


class ArgumentException(Exception):
    
    def __str__(self, *args):
        return f'Arguments {args} error!'


class ExcelException(Exception):
    
    def __str__(self, arg):
        if type(arg).__base__ is Exception:
            return str(arg)
        elif isinstance(arg, str):
            return 'Excel file IOError: ' + arg


class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "Error: %s" % msg
        
    def __str__(self):
        return self.msg


class IgnoreException(metaclass=WithLogger):
    
    def __init__(self, callback, *args, **kwargs):
        self.cb = callback
        self.args = args
        self.kwargs = kwargs
    
    def __enter__(self):
        '''
        捕获with语句异常
        '''        
        if self.cb:            
            try:
                return self.cb(*self.args, **self.kwargs)
            except:
                self.logger.debug(sys.exc_info()[1])
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        捕获body的异常
        '''
        if any([exc_type, exc_val, exc_tb]):
            self.logger.info(exc_val)
        return True # 不抛异常
