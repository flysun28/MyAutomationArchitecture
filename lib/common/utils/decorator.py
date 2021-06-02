'''
Created on 2021年5月29日
@author: 80319739
'''


def monitoring(cls):
    cls.monitored = True
    return cls


def singleton(cls):
    cls.singleton = True
    return cls