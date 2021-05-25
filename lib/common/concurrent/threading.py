# coding=utf-8
import time
import ctypes
from threading import Thread, ThreadError, _active
from lib.common.utils.meta import WithLogger
from six import with_metaclass
from lib.common.utils.misc_utils import timeit


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


class ExceptionMonitorThread(with_metaclass(WithLogger, Thread)):
    '''
    :param obj2exc: {obj:obj.errmsg, ...} mapping dictionary
    :param obj: the class instance which raised exception
    '''
    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls, *args, **kwargs)
        if getattr(cls, 'instance', None) is None:
            cls.instance = self
        return cls.instance

    def __init__(self, interval=0.01, **kwargs):
        self.interval = interval
        name = kwargs.pop('name', '')
        self._name = name if name else self.__class__.__name__
        self.obj2exc = {}
        self.obj = None
        self._daemonic = kwargs.pop('daemon', True)
        self.is_terminate_self = False
        super().__init__(kwargs=kwargs)
        self.start()
    
    @timeit
    def run(self):
        while True:
            if self.obj:
                errmsg = getattr(self.obj, 'exc', None) or getattr(self.obj, 'errmsg', None)
                self.obj2exc.setdefault(self.obj, errmsg)
            time.sleep(self.interval)
            if _active and self.is_terminate_self:
                all_active_thrs = list(_active.values())
                for t in all_active_thrs.copy():
                    kill_thread(t)
                    all_active_thrs.remove(t)
                assert not all_active_thrs, [t._target for t in all_active_thrs]
                # _active可能并未清空，还剩有None，原因未知，这里强制清空 ------ 坑-_-#
                _active.clear()
                break

            
def kill_thread(thr):
    '''
    Raises an exception in the thread `thr`
    :param thr: thread 
    '''
    tid = thr.ident
    if thr._target or thr._target == 'None':
        try:
            # 抛异常类型必须为SystemExit，否则子线程仍然不会退出，坑-_-#
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(SystemExit))
        finally:
            print('Thread {} is successfully killed with retcode={}'.format(thr._target, res))
            del _active[tid]
            if res == 0:
                raise ValueError("invalid thread id")
            elif res != 1:
                # if it returns a number greater than one, 
                # you should call it again with exc=NULL to revert the effect
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError("PyThreadState_SetAsyncExc failed")


monitor = ExceptionMonitorThread()

