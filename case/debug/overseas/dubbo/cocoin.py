#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/4/9 16:22
# comment:
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.globals import GlobalVar
server_info = GlobalVar.ZK_CLIENT_OUT.get_node_info("com.oppo.cocoin.facade.CocoinAccountOperationFacade")
conn = DubRunner(server_info['ip_port'][0], server_info['ip_port'][1])


def cocoin_in_come(ssoid, country, amount):
    """
    可币发放
    :return:
    """
    data = ssoid, country, amount, "TEST"
    result = conn.invoke(
        "com.oppo.cocoin.facade.CocoinAccountOperationFacade",
        "income",
        data,
        "STRING"
    )


if __name__ == '__main__':
    cocoin_in_come("2076075925", "VN", "10000")