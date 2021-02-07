# coding=utf-8

from itertools import product
from lib.common.utils import *
from lib.common.exception.intf_exception import ArgumentException

logger = Logger('接口参数遍历模板').get_logger()


class InterfaceExecStatistics():
    
    def __init__(self):
        self.PASS_NUM = 0
        self.FAIL_NUM = 0
        self.TOTAL = 0
        self.PASS_RATE = 0
    
    def __str__(self):
        return 'URL: %s\n' \
               'PASSED: %d\n' \
               'FAILED: %d\n' \
               'PASSED_RATE: %.2f%%' %(GlobarVar.HTTPJSON_IN.url, self.PASS_NUM, self.FAIL_NUM, self.PASS_NUM/self.TOTAL*100)
        

class InterfaceTestTemplate(metaclass=WithLogger):
    
    def __init__(self, callback):
        self.callback = callback
        self.statis = InterfaceExecStatistics()
    
    def positive_test(self, *varargs, stop_on_failure=False):
        varargs = to_iterable_nested(varargs, ele_type=tuple)
        print(50*'#' + '正向测试开始' + 50*'#')
        for idx, param_values in self._make_positive_test_values(varargs):
            self.logger.debug(param_values)
            self.statis.TOTAL += 1
            try:
                self.callback(*param_values)
                self.logger.info('No.%d %s\n%s --- PASS', idx, param_values, sys.exc_info()[1])
                self.statis.PASS_NUM += 1                
            except:
                self.logger.error('No.%d %s\n%s --- FAIL', idx, param_values, sys.exc_info()[1])
                self.statis.FAIL_NUM += 1
                if stop_on_failure:
                    raise ArgumentException(param_values)            
        self.logger.info(self.statis)
        print(50*'#' + '正向测试结束' + 50*'#')
    
    def negative_test(self, *varargs, stop_on_failure=False):
        varargs = to_iterable_nested(varargs, ele_type=tuple)
        print(50*'#' + '负向测试开始' + 50*'#')
        for idx, param_values in enumerate(product(*varargs), 1):
            if idx == 1:
                '第一列全为合法值，不参与异常参数遍历，仅作参照用'
                continue
            self.logger.debug(param_values)
            self.statis.TOTAL += 1
            try:
                self.callback(*param_values)
                self.statis.FAIL_NUM += 1
                self.logger.error('No.%d %s\n%s --- FAIL(期望失败，实际成功)', idx, param_values, sys.exc_info()[1])
                if stop_on_failure:
                    raise ArgumentException(param_values)
            except:
                self.statis.PASS_NUM += 1   
                self.logger.info('No.%d %s\n%s --- PASS(期望失败)', idx, param_values, sys.exc_info()[1])
        self.logger.info(self.statis)
        print(50*'#' + '负向测试结束' + 50*'#')
        
    def _make_positive_test_values(self, varargs):
        '创建嵌套列表'
        varargs = to_iterable_nested(varargs, ele_type=tuple)
        ext_varargs = extend_to_longgest(varargs)
        pos_values = list(zip(*varargs))
        self.logger.info(pos_values)
        return pos_values



