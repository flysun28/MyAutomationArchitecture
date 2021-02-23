'''
Created on 2021年2月8日
@author: 80319739
'''
import json
from collections import OrderedDict


class ExcelTestCase():
    CN_FDs = '用例名称', '用例标签', '用例类型', '请求报文体', '实际结果', '响应状态码', '期望结果', '用例执行结果', '备注'
    EN_FDs = 'name', 'tag', 'type', 'req_params', 'actual', 'status_code', 'expected', 'is_passed', 'comments'
#     FD_MAPPING = OrderedDict(zip(CN_FDs, EN_FDs))
    
    def __new__(cls, fields:tuple):
        cls.__slots__ = fields
        cls._validate_fields(fields)
        cls.__slots__ += 'id',
        self = object.__new__(cls)
        self._data = OrderedDict()
        return self
    
    @classmethod
    def _validate_fields(cls, fields:tuple):
        assert fields == cls.CN_FDs, ('\n', fields, '\n', cls.CN_FDs)

    def fill(self, values:tuple):
        for attr, value in zip(self.EN_FDs, values):
            if attr in ('req_params', 'expected') and value:
                value = json.loads(value)
            exec(f'self.{attr} = value')
            self._data[attr] = value
    
    def __str__(self):
        return str(dict(self._data))
    
    def __repr__(self):
        return 'ExcelTestCaseData: %s' %dict(self._data)
    
    @property
    def data(self):
        return self._data

    
    
