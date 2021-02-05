#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:10
# comment:
import hashlib


def sha_256(original_str):
    """
    :return:
    """
    s = hashlib.sha256()
    s.update(original_str.encode('utf-8'))
    return s.hexdigest()
