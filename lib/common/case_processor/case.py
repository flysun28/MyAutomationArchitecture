'''
Created on 2021年2月8日
@author: 80319739
'''
import json
import sys
from collections import OrderedDict
from lib.common.exception.intf_exception import IgnoreException


class ExcelTestCase():
    
    def __new__(cls, fields:tuple, protocol:str):
        cls.__slots__ = fields
        cls._validate_fields(fields)
        # set id and worksheet object as attr
        cls.__slots__ += ('id', 'ws')
        for item in sys.modules[cls.__module__].__dict__.values():
            if type(item) is type and item.__name__.endswith(protocol.capitalize()):  # item is class                
                break
        else:
            raise LookupError('ExcelTestCase{} class is not existed'.format(protocol.capitalize()))
        self = object.__new__(item)
        self._data = OrderedDict()
        self.file = None    # will be updated in CaseFile._generate_test_data
        return self
    
    @classmethod
    def _validate_fields(cls, fields:tuple):
        assert fields == cls.CN_FDs, ('\n', fields, '\n', cls.CN_FDs)

    def fill(self, values:tuple):
        for attr, value in zip(self.EN_FDs, values):
            if attr in ('req_params', 'expected', 'voucherInfo') and value:
                try:
                    value = json.loads(value)
                except json.decoder.JSONDecodeError:                    
                    # value is not a dictionary, pass directly
                    pass
            exec(f'self.{attr} = value')
            self._data[attr] = value
    
    def __str__(self):
        return str(dict(self._data))
    
    @property
    def data(self):
        return self._data


class ExcelTestCaseHttp(ExcelTestCase):
    CN_FDs = '用例名称', '用例标签', '用例类型', '请求报文体', '实际结果', '响应状态码', '期望结果', '用例执行结果', '备注'
    EN_FDs = 'name', 'tag', 'type', 'req_params', 'actual', 'status_code', 'expected', 'is_passed', 'comments'
    protocol = 'http'

    def __repr__(self):
        return 'ExcelTestCaseHttpData: %s' %dict(self._data)


class ExcelTestCaseDubbo(ExcelTestCase):
    CN_FDs = '用例名称', '用例标签', '用例类型', 'originalAmount', 'amount', 'kebiSpent', 'voucherInfo', 'payType',\
            '请求报文体', '实际结果', '响应状态码', '期望结果', '用例执行结果', '备注'
    EN_FDs = 'name', 'tag', 'type', 'originalAmount', 'amount', 'kebiSpent', 'voucherInfo', 'payType', \
            'req_params', 'actual', 'status_code', 'expected', 'is_passed', 'comments'
    protocol = 'dubbo'
    
    def __repr__(self):
        return 'ExcelTestCaseDubboData: %s' %dict(self._data)