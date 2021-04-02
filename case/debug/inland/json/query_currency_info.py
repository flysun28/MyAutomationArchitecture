#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/3/29 18:20
# comment:
import requests
from lib.common.utils.env import get_env_config

url = get_env_config()['url']['pay_in'] + "/nearme/QueryCurrencyInfo?" + "startPage=1&endPage=2&operate=add"
print("回调参数：{}".format(url))
response = requests.get(url)
result = response.content
print("返回结果：".format(result))

