#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/24 13:17
# comment:
import unittest
from case.scenario.inland.direct_pay import direct_pay


class Scenario(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_01(self):
        direct_pay(1, 1)

    def tearDown(self) -> None:
        pass

# if __name__ == '__main__':
#     suite = unittest.TestSuite()
#     suite.addTest(Scenario("test_01"))