#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/20 15:51
# comment:
import base64
from Lib.urllib.parse import quote
a = {"sdkVersionName":"2","sdkBuildTime":"1","sdkName":"UCBasic","headerRevisedVersion":1}
print(quote('{"sdkVersionName":"2","sdkBuildTime":"1","sdkName":"UCBasic","headerRevisedVersion":1}', encoding="utf-8"))