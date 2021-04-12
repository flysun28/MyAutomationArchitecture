import os
import re
import pytest
from lib.common.case_processor.entry import CaseFile
from lib.common.utils.globals import CASE_SRCFILE_ROOTDIR


# @pytest.fixture(scope='session', autouse=True)
def src_case_file(test_file_path):
    case_file_dir = os.path.join(CASE_SRCFILE_ROOTDIR, 'http')
    basename = os.path.basename(test_file_path)
    interface_name = re.search('test_(\w+)', basename, re.I).group(1)
    src_case_file = CaseFile(os.path.join(case_file_dir, 'inland.xlsx'), interface=interface_name)
    yield src_case_file
    src_case_file.save()
    src_case_file.close()