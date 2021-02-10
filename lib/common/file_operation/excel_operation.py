'''
@author: 80319739
'''
# import asyncio
from openpyxl import load_workbook, Workbook
from lib.common.concurrent.threading import ResultTakenThread
from lib.common.utils.meta import WithLogger


class Excel(metaclass=WithLogger):
    
    def __init__(self, path):
        self.path = path
        self.wb = None
#         self.wb = load_workbook(self.path, read_only=True)
        self.loading_thr = ResultTakenThread(load_workbook,
                                             self.path,
                                             read_only=True,
                                             daemon=True,
                                             name='LoadingExcelWorkbookThread')
        self.wb = self.loading_thr.result
        assert type(self.wb) is Workbook, 'invalid workbook obj %s' %self.wb
#         asyncio.run(self.loading_workbook())
#     
#     async def loading_workbook(self):
#         await load_workbook(self.path, read_only=True)
        
    def open_worksheet(self, name):
        return self.wb[name]
    
    def save(self):
        self.wb.save(self.path)
    
    def close(self):
        self.wb.close()

    