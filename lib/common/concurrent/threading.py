#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:32
# comment:

from threading import Thread, ThreadError
from six import with_metaclass
from lib.common.utils.meta import WithLogger


class ResultTakenThread(with_metaclass(WithLogger, Thread)):
    
    def __init__(self, target, *args, **kwargs):
        self._target = target
        self._args = args
        self._name = self.__class__.__name__
        self.result = None
        self._daemonic = kwargs.pop('daemon', False)
        self.is_error_raised = kwargs.pop('report_error', True)
    
    def run(self):
        try:
            self.result = self._target(*self._args, **self._kwargs)
        except ThreadError as e:
            if is_error_raised:
                raise ThreadError('%s exception: %s' %(self.name, e))
            else:
                self.logger.info(e)
        finally:
            del self._target, self._args, self._kwargs
    