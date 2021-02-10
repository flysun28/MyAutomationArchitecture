'''
@author: 80319739
'''
import os
import sys
from lib.common.case_processor.parser import ExcelParser
from lib.common.file_operation.excel_operation import Excel
from lib.common.file_operation.config_operation import Config
from lib.common.exception.intf_exception import NO_FILE_PARSER


class ExcelProxy():
     
    def __init__(self, path:str, interface:str=None):
        '''
        Excel proxy, associate with Excel fileobj and ExcelParser parser
        :param path: Excel file absolute path
        :param interface: the interface name, usually it's the last section of a URL
        '''
        self._fileobj = Excel(path)
        assert interface, f"Invalid interface name: {interface}, should be one of the worksheet names"
        ws = self._fileobj.open_worksheet(interface)
        self._parser = ExcelParser(ws)
    
    @property
    def fileobj(self):
        return self._fileobj
    
    @property
    def parser(self):
        return self._parser
    
    def actual_coord(self):
        return self._parser.actual_coord


class XMLProxy():
    pass


class Distributor():
    mapping_by_ext = {'xlsx': ExcelProxy, 'xml': XMLProxy, 'ini': Config}
    
    def __init__(self, path, *args, **kwargs):
        ext = os.path.splitext(path)[-1][1:]
        proxy_cls = self.mapping_by_ext.get(ext)
        if proxy_cls is ExcelProxy:
            assert 'interface' in kwargs or len(args)
        if proxy_cls is None:
            self.logger.error(20*'#' + ' No file parser found! ' + 20*'#')
            sys.exit(NO_FILE_PARSER)
        else:
            self.proxy = proxy_cls(path, *args, **kwargs)

    
    



