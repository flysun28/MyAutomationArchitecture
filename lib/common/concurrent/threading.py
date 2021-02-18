# coding=utf-8
import time
from threading import Thread, ThreadError
from lib.common.utils.meta import WithLogger
from six import with_metaclass


class ResultTakenThread(with_metaclass(WithLogger, Thread)):
    
    def __init__(self, target, *args, **kwargs):
        name = kwargs.pop('name', '')
        self._name = name if name else self.__class__.__name__
        self.result = None
        self._daemonic = kwargs.pop('daemon', False)
        self.is_error_raised = kwargs.pop('report_error', True)
        super().__init__(target=target, args=args, kwargs=kwargs)
        self.run()
    
    def run(self):
        try:
            while self.result is None or self.is_alive():
                self.result = self._target(*self._args, **self._kwargs)
                time.sleep(0.2)
        except ThreadError as e:
            if self.is_error_raised:
                raise ThreadError('%s exception: %s' %(self.name, e))
            else:
                self.logger.info(e)
        finally:
            del self._target, self._args, self._kwargs