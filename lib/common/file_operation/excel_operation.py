#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 22:57
# comment: excel操作

from openpyxl import load_workbook
from lib.common.concurrent.threading import ResultTakenThread


class Excel():
    
    def __init__(self, path):
        self.path = path
        self.wb = None
        loading_thr = ResultTakenThread(load_workbook,
                                        self.path,
                                        read_only=True,
                                        daemon=True,
                                        name='LoadingCaseExcelThread')
        if 
    