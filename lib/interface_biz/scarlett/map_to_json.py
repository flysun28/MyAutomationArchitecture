#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/4/25 13:22
# comment:
import json

a = "{charset=UTF-8, notify_time=2021-04-25 13:21:38, unsign_time=2021-04-25 13:21:38, alipay_user_id=2088112811111403, sign=IQzBbJZcuH9T5AgsbV+1Cefyppne3K8AmPMMxfv2vwVCdt94hMG2K40qeNT4bkv84yJbSXjtwdiM9PNK0yyVUvRXH3/fuRdGTzzmexGf+sdZAqskavvCYud0JrOp4U7+SGzD0002lirXm+QeQarLw5Ppu7NkXdgQRhjFb85l4MtcZpxIay7JqHXC3IK6S2IwcZ1EIvk1cZTrfR7e8CtpfY+YGLf/HzZ1HbT6xAZcEl54fp0uM9rXOgXfejbOul/9eS1b8P5VEFPmQ/UR1oqEJEuWo4N4qwWpqYbkqO49aM7aonYP9muOHtS+EWCG1BMeEq2WXekJHy0+2cO3Z2nfig==, external_agreement_no=SN202104251121441327164428238554, version=1.0, notify_id=2021042500222132138017361420359661, notify_type=dut_user_unsign, agreement_no=20215225715271617440, auth_app_id=2016120904060189, personal_product_code=GENERAL_WITHHOLDING_P, app_id=2016120904060189, sign_type=RSA2, alipay_logon_id=156******06, status=UNSIGN, sign_scene=INDUSTRY|GAME_CHARGE}"


def scarlet_map_to_json(req):
    b = req.replace("=", '"="')
    c = b.replace(", ", '","')
    e = c.replace("{", '{"')
    f = e.replace("}", '"}')
    g = f.replace("=", ":")
    h = g.replace('":"":"",', '==", ')
    # print(eval(h), type(eval(h)))
    return eval(h)


if __name__ == '__main__':
    print(scarlet_map_to_json(a))