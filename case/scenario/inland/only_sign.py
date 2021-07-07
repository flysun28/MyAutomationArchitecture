import time
from case.scenario.common_req import ONLY_SIGN
from lib.common_biz.biz_db_operate import get_contract_code, update_sign_status
from lib.common_biz.choose_scarlett import choose_scarlett
from lib.common_biz.fiz_assert import FizAssert, is_assert
from lib.interface_biz.http.auto_re_new import AutoRenew
from lib.interface_biz.http.query_result import queryResult

req = ONLY_SIGN


def only_sign():
    """
    :return:
    """
    """
    【1】. 更新数据库状态为UNSIGN
    """
    update_sign_status(req.ssoid, req.pay_channel)
    """
    【2】. 调用签约接口，构造渠道回调报文
    """
    sign_order_info = AutoRenew(req.pay_channel, req.partner_id, req.interface_version, str(req.app_version),
                                req.renewProductCode, req.notify_url).only_sign()
    sign_request_id = sign_order_info['pay_req_id']
    contract_code = get_contract_code(sign_request_id)
    choose_scarlett(1, req.pay_channel, "", "SIGN", contract_code, partner_id=req.partner_id)
    """
    【3】. 查询支付结果
    """
    start = time.perf_counter()
    while time.perf_counter() - start < 5:
        try:
            query_res = queryResult(sign_request_id, "SIGN", pass_type="direct")
            assert query_res == '0000', '%s != 0000' %query_res
        except Exception as e:
            exc_value = e
            time.sleep(0.5)
        else:
            break
    else:
        raise TimeoutError('查询签约结果超时5s: %s!' %exc_value)
    """
    【4】.检查order表信息，无记录
    """
    """
    【5】.检查trade_order表信息，无记录
    """
    """
    【6】.检查autorenew_sign_info表信息
    """
    FizAssert().assert_auto_renew_sign_info(req.ssoid, req.pay_channel)
    """
    【7】.检查autorenew_sign_record表信息
    """
    FizAssert().assert_auto_renew_sign_record(sign_request_id)
    """
    【8】.检查表notify_info信息
    """
    FizAssert().assert_notify(sign_order_info["partner_code"], 0, pay_type="sign")


if __name__ == '__main__':
    only_sign()
