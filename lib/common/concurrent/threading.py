# coding=utf-8
import time
import ctypes
import threading
from threading import Thread, ThreadError, _active, _main_thread
from lib.common.utils.misc_utils import timeit

    
class ResultTakenThread(Thread):
    
    def __init__(self, target, *args, **kwargs):
        name = kwargs.pop('name', '')
        self._name = name if name else self.__class__.__name__
        self.result = None
        self._daemonic = kwargs.pop('daemon', True)
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


class ExceptionMonitorThread(Thread):
    '''
    :param obj2exc: {obj:obj.errmsg, ...} mapping dictionary
    :param obj: the instance(e.g. HttpJsonSession/EncryptJson/DubRunner) which raised exception
    '''

    def __init__(self, interval=0.01, **kwargs):
        self.interval = interval
        name = kwargs.pop('name', '')
        self._name = name if name else self.__class__.__name__
        self.init_common()
        self.obj2exc = {}
        super().__init__(daemon=kwargs.pop('daemon', True), kwargs=kwargs)
        self.start()
    
    def init_common(self):
        self.obj = None
        self.case = None
        self.is_terminate_self = False
    
    @timeit
    def run(self):
        while True:
            if self.obj:
                # 监听self.obj，更新self.obj2exc
                errmsg = getattr(self.obj, 'exc', None) or getattr(self.obj, 'errmsg', None)
                self.obj2exc.setdefault(self.obj, errmsg)
                if self.case:
                    self.case.is_passed = 'failed'
            time.sleep(self.interval)
#             if self.is_terminate_self:
#                 # 终止所有线程
#                 kill_all_active_threads()
#                 break

    def reset(self, is_all=False):
        if is_all:
            self.obj2exc.clear()
        elif self.obj:        
            self.obj2exc.pop(self.obj, '')
            self.obj.errmsg = ''
        self.init_common()


def _kill_thread(thr):
    '''
    Raises an exception in the thread `thr`
    :param thr: thread 
    '''
    tid = thr._ident
    try:
        # 抛异常类型必须为SystemExit，否则子线程仍然不会退出 ------ 坑-_-#
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(SystemExit))
    except BaseException as e:
        print('Trying to kill {} raised exception {}'.format(thr, e))
        raise
    else:     
        print('Thread {} is successfully killed with retcode={}'.format(thr._target, res))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # if it returns a number greater than one, 
            # you should call it again with exc=NULL to revert the effect
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    finally:
        del _active[tid]


def kill_all_active_threads():
    active = threading.enumerate()
    for t in active.copy():
        if t is not _main_thread:
            _kill_thread(t)
            active.remove(t)


def get_nondaemon_threads():
    while True:
        active = threading.enumerate()
        for t in active:
            if t is not _main_thread and t._daemonic is False:
                break
        else:
            break
        time.sleep(2)


# 全局监听线程，监控http/dubbo请求是否异常，有异常则保存异常信息，后供pytest_runtest_makereport用
monitor = ExceptionMonitorThread()
