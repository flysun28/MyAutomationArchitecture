#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:09
# comment:
import hashlib


def md5(original_str, to_upper=True):
    """
    :return:
    """
    m = hashlib.md5()
    m.update(original_str.encode(encoding='UTF-8'))
    md5_str = m.hexdigest()
    if to_upper:
        return md5_str.upper()
    return md5_str


if __name__ == '__main__':
    print(md5("00"))