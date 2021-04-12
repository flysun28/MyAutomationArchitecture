'''
Created on 2021年2月8日
@author: 80319739
'''
from _functools import partial
from six import with_metaclass
from abc import ABCMeta, abstractmethod
from _collections_abc import _check_methods
from openpyxl.worksheet.worksheet import Worksheet
from lib.common.utils.meta import WithLogger
from .case import ExcelTestCase
 

class Parser(metaclass=ABCMeta):
    
    def __iter__(self):
        finished = yield from self.generate()
        finished = 'Yes' if finished else 'No'
        self.logger.info('Are all cases in <Worksheet "%s"> are generated? %s' %(self.ws.title, finished))
        
    @abstractmethod
    def parse(self, *args, **kwargs):
        raise NotImplementedError
    
    generate = partial(parse, to_iter=True)
    
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Parser:
            return _check_methods(C, "parse")
        return NotImplemented


class ExcelParser(with_metaclass(WithLogger, Parser)):
    
    def __init__(self, ws:Worksheet):
        self.ws = ws
        self._actual_coord = None
        self.init()
    
    def parse(self, to_iter=False):
        self.init()
        for row in self.ws.iter_rows(self.ws.min_row, self.ws.max_row,
                                     self.ws.min_column, self.ws.max_column,
                                     values_only=False):
            # row is a tuple
            if row[0].value == '用例名称':
                self._is_case_started = True
                self.fields = tuple(cell.value for cell in row)
                self.actual_coord = row
                continue
            if self._is_case_started:
                _case = ExcelTestCase(self.fields)
                _case.ws = self.ws
                _case.fill(cell.value for cell in row)
                if to_iter:
                    yield _case
                else:
                    self.cases.append(_case)
        return True

    def init(self):
        self.fields = None
        self._is_case_started = False
        self.cases = []
    
    @property
    def actual_coord(self):
        return self._actual_coord
    
    @actual_coord.setter
    def actual_coord(self, fd_row):
        for cell in fd_row:
            if cell.value == '实际结果':
                self._actual_coord = cell.coordinate
                print('实际结果坐标:', self.actual_coord)
                break
        
