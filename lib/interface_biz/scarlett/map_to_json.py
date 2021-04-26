#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/4/25 13:22
# comment:
import json
import re


def _scarlet_map_to_json(req):
    b = req.replace("=", '"="')
    c = b.replace(", ", '","')
    e = c.replace("{", '{"')
    f = e.replace("}", '"}')
    g = f.replace("=", ":")
    h = g.replace('":"":"",', '==", ')
    return eval(h)


def scarlet_map_to_json(req):
    imatches = re.finditer('(.*?)(,|})\s*', req[1:])
    for m in imatches:
        pair = m.group(1)
        left, _, right = pair.partition('=')
        left = '"' + left.strip() + '"'
        right = '"' + right.strip() + '"'
        repl = ''.join([left, ': ', right])
        req = req.replace(pair, repl)
    return req


if __name__ == '__main__':
    a = '{charset=UTF-8, notify_time=2021-04-26 11:26:35, alipay_user_id=2088202596648570, sign=NiiXCW16BvKX9hxixPlxqxhAAU+Rj9LaUU26TZTmE+VUFo+pHGEAxE1ubfjBBiGL7+rh9mtK3n+If1jyeOE9XNeQWeHNXihJYUjLnbnWhf57e7kpKvJW+wjZLqt+xKlmYnpWBcKyzjn7lTR8EWlkim/MpOyBAQU5rhNDZPGzN9AWx8pI9FTO/cK2gw+Wq8J1SDD9vX/4mn1f2rjIozDmiTrmKc+Q9ir/gHQ2ows9YP3Remx/IdlKsa7lzaUWXQo8o3Zh8fNKvnZG0EnEbSkaO7JZCrIIz0/OKp6/1tf9Ks7JYkwmsKcGi0MfoZ2Ej/9pIJNeOhUJcEvTbauym+uTAw==, external_agreement_no=SN202104261125516785511073180072, version=1.0, sign_time=2021-04-26 11:26:35, notify_id=2021042600222112635013531415389971, notify_type=dut_user_sign, agreement_no=20215226712418230557, auth_app_id=2016120904060189, invalid_time=2115-02-01 00:00:00, personal_product_code=GENERAL_WITHHOLDING_P, valid_time=2021-04-26 11:26:35, app_id=2016120904060189, sign_type=RSA2, alipay_logon_id=280***@qq.com, status=NORMAL, sign_scene=INDUSTRY|GAME_CHARGE}'
    print(scarlet_map_to_json(a))