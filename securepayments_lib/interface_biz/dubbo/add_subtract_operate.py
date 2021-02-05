#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2020/9/3 14:25
# comment: 可币发放与扣除
from Assembly.runner.dubbo_runner import DubRunner
from Common.common.random_order import get_random_number
from Common.tools.log.print_log import LogInfo

logger = LogInfo('dubbo-可币发放与扣除').get_log()


def nearme_add_subtract(host, amount, ssoid, operate_type):
    """
    可币发放与扣除
    :param amount: 单位：元
    :param ssoid:
    :param operate_type:
    :return:
    """
    # 10.177.43.129 10.177.160.60 10.177.159.14
    conn = DubRunner(host, 22880)
    data = {
        "amountMoney": amount,
        "batchId": get_random_number(32),
        "bizNo": get_random_number(32),
        # PRESENT 发放  DEDUCT  扣除
        "operateType": operate_type,
        "requestId": get_random_number(32),
        "source": "后台",
        "ssoid": ssoid,
        "timeStamp": 2020
    }
    result = conn.invoke(
        "NearmeAccountOperate",
        "addSubtractOperate",
        data
    )    
    logger.info('返回的结果：{}'.format(result.encode("GBK", "ignore")))
    


if __name__ == '__main__':
    nearme_add_subtract('10.177.159.14', "0.019", "2086100900", "PRESENT")    #test3
#     nearme_add_subtract('10.177.159.14', "0.03", "2086100900", "DEDUCT")    #test3
#     nearme_add_subtract('10.177.110.171', "1", "2086100900", "PRESENT")     #test1
#     nearme_add_subtract('10.177.110.171', "6", "2086100900", "DEDUCT")

