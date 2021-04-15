'''
@author: 80319739
'''
from six import with_metaclass
from lib.common.utils.meta import WithLogger
from lib.common.exception.intf_exception import ExcelException
from lib.common.case_processor.proxy import Distributor
from lib.common.utils.misc_utils import to_iterable, get_letter_seqno
from itertools import chain


class CaseFile(with_metaclass(WithLogger)):
    
    def __init__(self, path, *args, **kwargs):
        self.proxy = Distributor(path, *args, **kwargs).proxy
        self.parser_ref = self.proxy.parser
        self._pos_tc = {}
        self._neg_tc = {}
        self._all_tc = {}
        self._case_name_to_actual = {}
    
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
        return self.positive_cases + self.negative_cases
    
    def one_case(self, case_name):
        if not self._all_tc:
            self._generate_test_data()
        return self._all_tc[case_name]
    
    @property
    def positive_cases(self):
        if not self._pos_tc:
            self._generate_test_data()
        self.logger.info('正向测试用例数据：')
        pos_tc = list(self._pos_tc.values())
        for tc in pos_tc:
            self.logger.info(dict(tc.data))
        return pos_tc
    
    @property
    def negative_cases(self):
        if not self._neg_tc:
            self._generate_test_data()
        self.logger.info('负向测试用例数据：')
        neg_tc = list(self._neg_tc.values())
        for tc in neg_tc:
            self.logger.info(dict(tc.data))
        return neg_tc
    
    def update_actual(self, case_name, actual):
        actual_title_coord = self.parser_ref.actual_coord    # E6
        start_row = int(actual_title_coord[1:]) + 1
        end_column = get_letter_seqno(actual_title_coord[0])
        for row in self.parser_ref.ws.iter_rows(start_row, self.parser_ref.ws.max_row,
                                                self.parser_ref.ws.min_column, end_column,
                                                values_only=False):
            if row[0].value == case_name:
                actual_coord = actual_title_coord[0] + row[0].coordinate[1:]
                print('"%s"实际结果坐标: %s' %(case_name, actual_coord))
                self._case_name_to_actual[case_name] = actual_coord
                break
        else:
            raise LookupError('用例数据查找失败，请确认输入的用例名称。')
        self.parser_ref.ws[actual_coord] = actual
        self.save()
    
    def update_running_result(self, outcome:str):       
        result_title_coord = self.parser_ref.running_result_coord
        if not result_title_coord:
            return
        start_row = int(result_title_coord[1:]) + 1
        end_column = get_letter_seqno(result_title_coord[0])
        for row in self.parser_ref.ws.iter_rows(start_row, self.parser_ref.ws.max_row,
                                                self.parser_ref.ws.min_column, end_column,
                                                values_only=False):
            if row[0].value in self._case_name_to_actual:
                _name = row[0].value
                row_num = self._case_name_to_actual[_name][1:]  #获取行号
                result_coord = result_title_coord[0] + row_num
                print('"%s"用例执行结果坐标: %s' %(_name, result_coord))
                self.parser_ref.ws[result_coord] = outcome
        self.save()
        
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

