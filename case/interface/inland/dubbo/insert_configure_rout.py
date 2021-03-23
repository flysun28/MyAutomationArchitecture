#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/17 22:25
# comment: 开放网关路由配置sql, 默认app_id=000000
import os
import time
from lib.common.file_operation.excel_operation import Excel
from lib.common.logger.logging import Logger
from lib.common.utils.globals import GlobalVar
local_time = time.strftime("%Y-%m-%d %H:%M:%S")
# 新增appId SQL(一般不执行)
add_app_id = "INSERT INTO `db_platform_gateway`.`server_app_info` VALUES (NULL,'platform-gateway','平台网关','000000'," \
             "'测试专用','i3neUaFj5ybxDJ7TLgrial4mbpAjmjen','xiaoyao1@oppo.com','NORMAL','xiaoyao'," \
             "'{}','{}',NULL,'')".format(local_time, local_time)


mysql = GlobalVar.MYSQL_IN
logger = Logger('parser_dubbo').get_logger()


def parser_dubbo_excel():
    """
    解析dubbo_info
    :return:
    """
    # excel信息
    project_path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
    project_path.replace('\\', '/')
    dubbo_server_path = os.path.join(project_path, 'dubbo/', 'dubbo_info.xlsx')
    sheet = Excel(dubbo_server_path).open_worksheet("Sheet1")
    max_row = sheet.max_row
    max_column = sheet.max_column
    list_all_info = []
    for i in range(2, max_row+1):
        temp_data = []
        for j in range(1, max_column+1):
            b = sheet.cell(i, j).value
            temp_data.append(b)
        list_all_info.append(temp_data)
    return list_all_info


def insert_one(interfaceName, method, parameter_types):
    """
                                                                                                  | -->若已添加，无需添加
                                                            |-->若已添加   查询是否已经添加了路由信息 |
                                                           |                                      |-->若未添加，添加路由信息
    先判断`dubbo_service_info`表中是否已经添加了dubbo接口信息 |
                                                          |-->若未添加   添加接口信息 再添加路由信息
    :param interfaceName: 接口名称
    :param method: 方法名称
    :param parameter_types: 参数列表
    :return:
    """
    # 查询方法是否被添加/返回新增方法id
    select_server_id = 'SELECT id FROM `db_platform_gateway`.`dubbo_service_info` WHERE method = "{}" ORDER BY id DESC ' \
                       'LIMIT 1'.format(method)
    server_id = mysql.select(select_server_id)
    if server_id == ():
        # 新增服务信息配置 SQL（先执行）
        add_server_info = "INSERT INTO `db_platform_gateway`.`dubbo_service_info` VALUES (NULL, 'platform-test','{}'," \
                          "'{}','{}','3000','0','DefaultDubboInvoker','','',NULL,'', '{}','{}')".\
            format(interfaceName, method, parameter_types, local_time, local_time)
        mysql.execute(add_server_info)
        server_id = mysql.select(select_server_id)[0]['id']
        # 新增路由配置 SQL（后执行）
        add_rout_info = "INSERT INTO `db_platform_gateway`.`request_route_info` VALUES(NULL,'000000','batchGrant'," \
                        "'1.0', 'DUBBO','','{}','','',NULL,NULL,'{}','{}')".format(server_id, local_time, local_time)
        mysql.execute(add_rout_info)
    else:
        server_id = mysql.select(select_server_id)[0]['id']
        # 查询路由是否配置，注意：request_route_info 中的service字段默认写method
        select_is_route = 'SELECT service FROM `db_platform_gateway`.`request_route_info` WHERE app_id="000000" AND ' \
                          'dubbo_service_id = "{}" AND service = "{}"'.format(server_id, method)
        is_route = mysql.select(select_is_route)
        if is_route == ():
            add_rout_info = "INSERT INTO `db_platform_gateway`.`request_route_info` VALUES(NULL,'000000','{}'," \
                            "'1.0', 'DUBBO','','{}','','',NULL,NULL,'{}','{}')".format(method, server_id, local_time,
                                                                                       local_time)
            mysql.execute(add_rout_info)
        else:
            logger.info("路由信息已添加，无需添加")


def insert_batch():
    """
    通过excel批量导入服务信息，批量写入
    excel解析格式(列表嵌套列表)：
    [["", "", "", "", ""], ["", "", "", "", ""], ....]
    :return:
    """
    dubbo_info = parser_dubbo_excel()
    for item in dubbo_info:
        if item[4] == "OK":
            logger.info("excel标识路由信息已添加，无需添加")
        else:
            insert_one(item[1], item[2], item[3])


if __name__ == '__main__':
    #insert_one("com.oppo.voucher.api.CouponBatchGrant", "batchGrant", "com.oppo.voucher.api.req.CouponBatchGrantReqDto")
    insert_batch()
