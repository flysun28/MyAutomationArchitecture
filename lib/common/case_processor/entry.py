'''
@author: 80319739
'''
import os
import re
import time
import simplejson
from itertools import chain
from six import with_metaclass
from lib.common.utils.meta import WithLogger
from lib.common.exception.intf_exception import ExcelException
from lib.common.case_processor.proxy import Distributor
from lib.common.utils.misc_utils import to_iterable, get_letter_seqno, timeit
from lib.common.utils.globals import CASE_SRCFILE_ROOTDIR
from lib import pardir


class CaseFile(with_metaclass(WithLogger)):
    
    def __init__(self, path, *args, **kwargs):
        self.path = path
        self.sheetname = kwargs.get('interface', '')
        self.proxy = Distributor(path, *args, **kwargs).proxy
        self.parser_ref = self.proxy.parser
        self.parser_ref.protocol = os.path.basename(pardir(path))
        self._pos_tc = {}
        self._neg_tc = {}
        self._all_tc = {}
        self._case_to_coord = {}  # 用例名称：坐标
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        exc_args = exc_type, exc_val, exc_tb
        if any(exc_args):
            raise ExcelException(exc_val)
        else:
            self.proxy.fileobj.close()
    
    def __str__(self):
        return 'CaseFile: '+self.path
    
    def parse(self):
        yield from self.parser_ref.parse(to_iter=True)
    
    def __iter__(self):
        yield from self.parse()

    def _generate_test_data(self):
        if self._all_tc:
            return
        to_iterable(self.parser_ref.parse(), tuple)
        for case in self.parser_ref.cases:
            if case.type == '+':
                self._pos_tc[case.name] = case
            elif case.type == '-':
                self._neg_tc[case.name] = case
            case.file = self
        self._all_tc.update(self._pos_tc)
        self._all_tc.update(self._neg_tc)
    
    @property
    def all_cases(self):
        self._generate_test_data()
#         return self.positive_cases + self.negative_cases
        return list(chain(self._pos_tc.values(), self._neg_tc.values()))
    
    def one_case(self, case_name):
        self._generate_test_data()
        return self._all_tc[case_name]

    @property
    def positive_cases(self):
        self._generate_test_data()
        self.logger.info('正向测试用例数据：')
        pos_tc = list(self._pos_tc.values())
        for tc in pos_tc:
            self.logger.info(dict(tc.data))
        return pos_tc
    
    @property
    def negative_cases(self):
        self._generate_test_data()
        self.logger.info('负向测试用例数据：')
        neg_tc = list(self._neg_tc.values())
        for tc in neg_tc:
            self.logger.info(dict(tc.data))
        return neg_tc
    
    @timeit
    def writeback(self, case_name, value, ref_coord):
        self.logger.info('开始更新"{}"[{}]={}'.format(case_name, ref_coord, value))
        start_row = int(ref_coord[1:]) + 1
        end_column = get_letter_seqno(ref_coord[0])
        for row in self.parser_ref.ws.iter_rows(start_row, self.parser_ref.ws.max_row,
                                                self.parser_ref.ws.min_column, end_column,
                                                values_only=False):
            if row[0].value == case_name:
                upd_coord = ref_coord[0] + row[0].coordinate[1:]
                self._case_to_coord.setdefault(case_name, upd_coord)
                break
        else:
            raise LookupError('用例数据查找失败，请确认输入的用例名称。')
        value = simplejson.dumps(value, ensure_ascii=False).strip('"')
        self.parser_ref.ws[upd_coord] = value
#         self.save()
    
    def update_actual(self, case_name, actual):
        self.writeback(case_name, actual, self.parser_ref.actual_coord)

    def update_req(self, case_name, req):
        self.writeback(case_name, req, self.parser_ref.req_coord)
    
    def update_running_result(self, case_name, outcome:str):       
        self.writeback(case_name, outcome, self.parser_ref.running_result_coord)
     
    def update_voucher_info(self, case_name, vouinfo):
        self.writeback(case_name, vouinfo, self.parser_ref.voucher_coord)

    def save(self):
        self.proxy.fileobj.save()
        time.sleep(1)

    def close(self):
        self.proxy.fileobj.close()


def src_case_file(test_file_path):
    protocol = re.search('http|dubbo|protobuf', test_file_path, re.I).group()
    case_file_dir = os.path.join(CASE_SRCFILE_ROOTDIR, protocol)
    basename = os.path.basename(test_file_path)
    interface_name = re.search('test_(\w+)', basename, re.I).group(1)
    case_file = CaseFile(os.path.join(case_file_dir, 'inland.xlsx'), interface=interface_name)
    print(case_file)
    return case_file


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

