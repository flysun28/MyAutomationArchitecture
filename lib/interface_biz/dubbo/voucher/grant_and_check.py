#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2020/12/23 14:52
# comment:
from Pay.case.inland.debug.dubbo_tools.voucher.checkVoucher import checkVoucher
from Pay.case.inland.debug.dubbo_tools.voucher.grantVoucher import grantVoucher

# 折扣券
batchId = grantVoucher('10.177.158.19', "2031", "KB_COUPON", "DAZHE", "1", "0", "2086100900", 0.01, '0.99')
checkVoucher(batchId)

# 满减券
# batchId = grantVoucher('10.177.43.135', "5456925", "KB_COUPON", "DIKOU", "1", "0.98", "2086100900")
batchId = grantVoucher('10.177.158.19', "2031", "KB_COUPON", "DIKOU", "1", "0.98", "2086100900")
checkVoucher(batchId)

# 消费券
batchId = grantVoucher('10.177.158.19', "2031", "KB_COUPON", "XIAOFEI", "10", "9", "2086100900")
checkVoucher(batchId)

# 消费折扣
batchId = grantVoucher('10.177.158.19', "2031", "KB_COUPON", "XIAOFEI_DAZHE", "1", "0", "2086100900", 0.1, "10")
checkVoucher(batchId)
