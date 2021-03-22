#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/16 15:05
# comment: 未调通
import requests
from lib.common.logger.logging import Logger
from lib.common.utils.env import get_env_config
logger = Logger('adney-scarlet').get_logger()

scarlett_data = {
   "live": "false",
   "notificationItems": [
      {
         "NotificationRequestItem": {
            "additionalData": {},
            "eventCode": "AUTHORISATION",
            "success": "true",
            "eventDate": "2019-06-28T18:03:50+01:00",
            "merchantAccountCode": "YOUR_MERCHANT_ACCOUNT",
            "pspReference": "7914073381342284",
            "merchantReference": "YOUR_REFERENCE",
            "amount": {
                "value": 1130,
                "currency": "EUR"
            }
         }
      }
   ]
}
print(get_env_config()['url']['pay_scarlet_out'] + "/opaycenter/adyenNotify")
response = requests.post(get_env_config()['url']['pay_scarlet_out'] + "/opaycenter/adyenNotify", scarlett_data)
print(response.status_code)
result = response.content
logger.info("返回结果：{}".format(result))
