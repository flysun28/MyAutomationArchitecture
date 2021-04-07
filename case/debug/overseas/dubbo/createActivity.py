#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/30 14:16
# comment:
from lib.common.session.dubbo.dubbo import DubRunner
from lib.common.utils.env import get_dubbo_info
from lib.common.utils.globals import GlobalVar

dubbo_info = get_dubbo_info("activity", in_out="oversea")
conn = DubRunner(dubbo_info[0], dubbo_info[1])


def create(flag):
    data = {}
    if flag == "1":
        # 满减
        data = {
            "activityId": 0, "bizNo": 5456925, "activityName": "auto_create_MANJIAN", "startTime": "2021-03-27 21:30:00",
            "endTime": "2021-04-09 21:30:00",
            "discountType": "MANJIAN", "totalAmount": 100000, "totalNum": 5,
            "creater": "80264408", "operateType": "CREATE", "currency": "INR", "country": "IN",
            "allowTimes": 1,
            "mono": "auto_create_mo", "channelType": "codapay_paytm", "amountType": "ACTIVITY", "activityType": "YOUHUI",
            "userType": "ALL_USERS",
            "totalAttendTimes": 1,
            "payActionType": "ALL", "createJson": "{}", "hasPackageLimit": "Y", "hasUserLimit": "Y",
            "discountInfo": {"cutAmount": 500, "fullAmount": 1000, "discountType": "MANJIAN"},
            "cutAmount": 500,
            "full_amount": 1000,
            "class": "com.oppo.payactivity.api.dto.ActivityOperateReq"
        }
    if flag == "2":
        data = {"activityId": 0, "bizNo": 5456925, "activityName": "auto_create_DAZHE", "startTime":"2021-03-27 21:30:00",
                "endTime": "2021-04-09 21:30:00",
                "discountType": "DAZHE", "totalAmount": 1000, "totalNum": 5,
                "creater": "80264408", "operateType": "CREATE", "currency": "INR", "country": "IN",
                # 是否允许多次使用
                "allowTimes": 0,
                "mono": "gddsgdsgdsgds", "channelType": "codapay_paytm", "amountType":  "ACTIVITY",
                "activityType": "YOUHUI","userType": "ALL_USERS",
                "totalAttendTimes": 1,
                "payActionType": "ALL", "createJson": "{}", "hasPackageLimit": "Y", "hasUserLimit": "Y",
                "discountInfo": {"rate": 80, "maxCutAmount": 400, "minConsAmount": 500, "discountType": "DAZHE"},
                "class": "com.oppo.payactivity.api.dto.ActivityOperateReq"}
    result = conn.invoke(
        "com.oppo.payactivity.api.facade.ActivityOperate",
        "createActivity",
        data
    )
    return result['object']['activityId']


def create_white_list(activityId):
    data = {
        "activityId": activityId,
        # "com.example.pay_demo"
        "packageList": ["com.example.pay_demo"],
        # "2076075925", "2086628989"
        "ssoidList": ["2076075925"],
        # "000000000000000"
        "imeiList": ["000000000000000"],
        # "FBC4E853B36C40C8A2AC61D127D85C9E23fe8cbbef964f0009fa0ac296d07836"
        "openIdList": ["FBC4E853B36C40C8A2AC61D127D85C9E23fe8cbbef964f0009fa0ac296d07836"]
    }
    result = conn.invoke(
        "com.oppo.payactivity.api.facade.ActivityWhiteService",
        "createActivityWhiteList",
        data)


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
    list_id = [192]
    for item in list_id:
        activity_off(item)
    activity_id = create("1")
    create_white_list(activity_id)
    activity_pass(activity_id)
