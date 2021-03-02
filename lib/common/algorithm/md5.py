#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:09
# comment:
import hashlib


def md5(original_str, to_upper=True):
    """
    :return:
    """
    m = hashlib.md5()
    m.update(original_str.encode(encoding='UTF-8'))
    md5_str = m.hexdigest()
    if to_upper:
        return md5_str.upper()
    return md5_str


if __name__ == '__main__':
    print(md5("appid=1104946420&mch_id=1282256301&nonce_str=5d9062b72e65846f8b9b0a6e176ecce9&openid=0D4E5B0D1AE1605ADD7EECFCA611DC84&out_refund_no=20210302213427592561556242617421&out_trade_no=RM202103022132002076075925615562&refund_channel=ORIGINAL&refund_fee=1&refund_id=12822563017012202103021639413456&result_code=SUCCESS&retcode=0&retmsg=ok&return_code=SUCCESS&return_msg=SUCCESS&total_fee=1&transaction_id=12822563016012202103021548430031&key=46b3da6ee122993430adb1f7e20c4327"))
    print(md5("appid=1104946420&mch_id=1104946420&nonce_str=5d9062b72e65846f8b9b0a6e176ecce9&openid=0D4E5B0D1AE1605ADD7EECFCA611DC84&out_refund_no=20210302213427592561556242617421&out_trade_no=RM202103022132002076075925615562&refund_channel=ORIGINAL&refund_fee=1&refund_id=12822563017012202103021639413456&result_code=SUCCESS&retcode=0&retmsg=ok&return_code=SUCCESS&return_msg=SUCCESS&total_fee=1&transaction_id=12822563016012202103021548430031&key=46b3da6ee122993430adb1f7e20c4327"))
