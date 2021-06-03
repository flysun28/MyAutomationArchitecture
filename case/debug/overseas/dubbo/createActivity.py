#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/30 14:16
# comment:
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.globals import GlobalVar
from lib.common_biz.order_random import RandomOrder

server_info = GlobalVar.ZK_CLIENT_OUT.get_node_info("com.oppo.payactivity.api.facade.ActivityWhiteService")
conn = DubRunner(server_info['ip_port'][0], server_info['ip_port'][1])


def create(flag, isLimit="Y", userLimit="Y"):
    data = {}
    if flag == "1":
        # 满减
        data = {
            "activityId": 0, "bizNo": 5456925, "activityName": "auto_create_MANJIAN" + RandomOrder(3).random_string(), "startTime": "2021-03-27 21:30:00",
            "endTime": "2023-04-09 21:30:00",
            "discountType": "MANJIAN", "totalAmount": 100000, "totalNum": 5,
            "creater": "80264408", "operateType": "CREATE", "currency": "INR", "country": "IN",
            "allowTimes": 1,
            "mono": "auto_create_mo", "channelType": "codapay_paytm", "amountType": "ACTIVITY", "activityType": "YOUHUI",
            "userType": "ALL_USERS",
            "totalAttendTimes": 1,
            "payActionType": "ALL", "createJson": "{}", "hasPackageLimit": isLimit, "hasUserLimit": userLimit,
            "discountInfo": {"cutAmount": 500, "fullAmount": 1000, "discountType": "MANJIAN"},
            "cutAmount": 500,
            "full_amount": 1000,
            "class": "com.oppo.payactivity.api.dto.ActivityOperateReq"
        }
    if flag == "2":
        data = {"activityId": 0, "bizNo": 5456925, "activityName": "auto_create_DAZHE", "startTime":"2021-03-27 21:30:00",
                "endTime": "2023-04-09 21:30:00",
                "discountType": "DAZHE", "totalAmount": 1000, "totalNum": 5,
                "creater": "80264408", "operateType": "CREATE", "currency": "INR", "country": "IN",
                # 是否允许多次使用
                "allowTimes": 0,
                "mono": "gddsgdsgdsgds", "channelType": "codapay_paytm", "amountType":  "ACTIVITY",
                "activityType": "YOUHUI","userType": "ALL_USERS",
                "totalAttendTimes": 1,
                "payActionType": "ALL", "createJson": "{}", "hasPackageLimit": isLimit, "hasUserLimit": userLimit,
                "discountInfo": {"rate": 80, "maxCutAmount": 400, "minConsAmount": 500, "discountType": "DAZHE"},
                "class": "com.oppo.payactivity.api.dto.ActivityOperateReq"}

    result = conn.invoke(
        "com.oppo.payactivity.api.facade.ActivityOperate",
        "createActivity",
        data
    )
    return result['object']['activityId']


"""
"activityId": activityId,
# "com.example.pay_demo"
"packageList": ["com.example.pay_demo"],
# "2076075925", "2086628989"
"ssoidList": ["2076075925"],
# "000000000000000"
"imeiList": ["000000000000000"],
# "FBC4E853B36C40C8A2AC61D127D85C9E23fe8cbbef964f0009fa0ac296d07836"
"openIdList": ["FBC4E853B36C40C8A2AC61D127D85C9E23fe8cbbef964f0009fa0ac296d07836"]
"""


def create_white_list(activityId, packageList, ssoidList, imeiList, openIdList):
    data = {
        "activityId": activityId,
        "packageList": packageList,
        "ssoidList": ssoidList,
        "imeiList": imeiList,
        "openIdList": openIdList

    }
    result = conn.invoke(
        "com.oppo.payactivity.api.facade.ActivityWhiteService",
        "createActivityWhiteList",
        data)


def create_black_list(activityId, b_ssoid, b_imei, b_openid):
    data = {"list": [
        {"activityId": activityId,
         "packageName": "",
         "ssoid": b_ssoid,
         "imei": b_imei,
         "openid": b_openid,
         "limitType": "BLACK"
         }
    ]}
    result = conn.invoke(
        "com.oppo.payactivity.api.facade.ActivityAdminService",
        "createActivityBlankList",
        str(data)
    )


def activity_pass(activityId):
    ID = GlobalVar.MYSQL_OUT.select_one(
        "select id from `opay_activity`.`activity_info` where activityId = {}".format(activityId))
    data = {
        "activityId": activityId,
        "id": ID['id'],
        "operator": "80264408",
        "reason": "1"
    }
    result = conn.invoke(
        "com.oppo.payactivity.api.facade.ActivityOperate",
        "activityPass",
        data)


def activity_off(activityId):
    data = {
        "activityId": activityId,
        "creater": "80264408",
        "reason": "1",
        "class": "com.oppo.payactivity.api.dto.ActivityOperateReq"
    }
    result = conn.invoke(
        "com.oppo.payactivity.api.facade.ActivityOperate",
        "activityOff",
        data)


if __name__ == '__main__':

    create_black_list(21, "2076075926", "0000000000000000001", "1111111111111111")
    # list_id = [22, 21, 17]
    # for item in list_id:
    #     activity_off(item)
    # activity_id = create("1")
    # create_white_list(activity_id)
    # activity_pass(activity_id)
