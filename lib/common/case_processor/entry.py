'''
@author: 80319739
'''
import os
import re
from six import with_metaclass
from lib.common.utils.meta import WithLogger
from collections import OrderedDict
from lib.common.exception.intf_exception import ExcelException
from lib.common.case_processor.proxy import Distributor
from lib.common.utils.misc_utils import to_iterable
from lib.common.utils.globals import CASE_SRCFILE_ROOTDIR


class CaseFile(with_metaclass(WithLogger)):
    
    def __init__(self, path, *args, **kwargs):
        self.proxy = Distributor(path, *args, **kwargs).proxy
        self.parser_ref = self.proxy.parser
        self._pos_tc = {}
        self._neg_tc = {}
        self._all_tc = {}
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        exc_args = exc_type, exc_val, exc_tb
        if any(exc_args):
            raise ExcelException(exc_val)
        else:
            self.proxy.fileobj.close()
            
    def parse(self):
        yield from self.parser_ref.parse(to_iter=True)
    
    def __iter__(self):
        yield from self.parse()

    def _generate_test_data(self):
        to_iterable(self.parser_ref.parse(), tuple)
        for case in self.parser_ref.cases:
            if case.type == '+':
                self._pos_tc[case.name] = case
            elif case.type == '-':
                self._neg_tc[case.name] = case
        self._all_tc.update(self._pos_tc)
        self._all_tc.update(self._neg_tc)
    
    @property
    def all_cases(self):
        if not self._all_tc:
            self._generate_test_data()
        return self._all_tc.values()
    
    def one_case(self, case_name):
        if not self._all_tc:
            self._generate_test_data()
        return self._all_tc[case_name]
    
    @property
    def positive_cases(self):
        if not self._pos_tc:
            self._generate_test_data()
        return self._pos_tc.values()
    
    @property
    def negative_cases(self):
        if not self._neg_tc:
            self._generate_test_data()
        return self._neg_tc.values()
    
    def update_actual(self, actual):
        coord = self.parser_ref.actual_coord
        self.parser_ref.ws[coord] = actual
    
    def save(self):
        self.proxy.fileobj.save()
        
    def close(self):
        self.proxy.fileobj.close()



if __name__ == '__main__':
    '''
    1. 创建统一的CaseFile类（上下文管理器和迭代器）作为入口
    2. CaseFile依赖Distributor类，负责按入参和文件扩展名适配到不同的Proxy类
    3. Proxy关联具体文件类（e.g. Excel）和文件解析器（e.g. ExcelParser）
    4. 文件解析器继承Parser，必须实现parse方法
    5. 文件解析器关联测试用例类（e.g. ExcelTestCase），保存用例数据，一行一条数据，
    6. CaseFile为迭代器，每次迭代返回一个ExcelTestCase实例
    7. 测试用例数据获取：
        1）ExcelTestCase实例.data
        2）直接打印ExcelTestCase实例
    '''
#     with CaseFile(r'E:\SecurePaymentsAutomation\case\src\case_excel\http_json.xlsx', interface='simplepay') as src:
    src = CaseFile(r'E:\SecurePaymentsAutomation\case\src\http\inland.xlsx', interface='simplepay')    
    for case in src:
        print(case)

