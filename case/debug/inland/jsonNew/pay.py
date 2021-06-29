'''
Created on 2021年5月31日
@author: 80319739
'''

from lib.interface_biz.http.refactor.pay import Pay


if __name__ == '__main__':
    pay = Pay()
    flag = 3
    if flag == 1:
        # 直扣
#         pay.direct_pay(1, 'wxpay')
#         pay.direct_pay(999999999, 'alipay')
#         pay.direct_pay(9999999999999999999999999999, 'alipay')  #解密请求失败
#         pay.direct_pay(1.2, 'wxpay')    #验签失败，amount被转成了1
#         pay.direct_pay(0, 'wxpay')    #商品原价要大于0
        pay.direct_pay_with_kb_negative(10, 'wxpay', '消费')  #直冲不能有优惠券和可币金额
#         pay.direct_pay_with_kb_negative(101, 'alipay', vou_key='抵扣', kb_spent=1)    #直冲不能有优惠券和可币金额
    if flag == 2:
        # 纯可币
        pay.only_kb_spend(1)
#         pay.only_kb_spend(2)    #余额不足
    if flag == 3:
        # 纯可币券
        pay.only_voucher_spend(2, '消费', voucherCount=1, voucherDeductAmount=2)
#         pay.only_voucher_spend(1, '消费', voucherCount=4, voucherDeductAmount=2)  #支付金额不能为负数
    if flag == 4:
        # 纯可币+可币券
        pay.only_kb_voucher_spend(100, '折扣')
    if flag == 5:
        # 可币+渠道
        pay.channel_kb_pay(10, 'wxpay')
    if flag == 6:
        # 可币券+渠道
        pay.channel_voucher_pay(10, 'wxpay', '消费')
#         pay.channel_voucher_pay(101, 'alipay', '抵扣')
#         pay.channel_voucher_pay(10, 'alipay', '抵扣')  #券未达到条件金额
#         pay.channel_voucher_pay(101, 'wxpay', '折扣')
#         pay.channel_voucher_pay(100, 'alipay', '消费折扣')
#         pay.channel_voucher_pay(1001, 'wxpay', '红包')
#         pay.channel_voucher_pay(10, 'alipay', '红包')    #券未达到条件金额
    if flag == 7:
        # 可币+可币券+渠道
#         pay.channel_kb_voucher_pay(10, 'wxpay', '消费')
        pay.channel_kb_voucher_pay(10, 'wxpay', '消费')
#         pay.channel_kb_voucher_pay(101, 'alipay', '抵扣', kb_spent=1)
#         pay.channel_kb_voucher_pay(10, 'alipay', '抵扣', kb_spent=1)  #支付金额不能为负数（正向下单不核销券）
#         result = pay.channel_kb_voucher_pay(101, 'wxpay', '折扣', kb_spent=1)
#         result = pay.channel_kb_voucher_pay(90, 'wxpay', vou_key=100935200, kb_spent=1) #正向下单不核销券
#         choose_scarlett(1, 'wxpay', result['data']['payRequestId'], partner_id=pay.partner_id)  #微信回调，期望支付中心核销券失败，走自动退款流程
#         pay.channel_kb_voucher_pay(1000, 'alipay', '消费折扣')
#         result = pay.channel_kb_voucher_pay(2000, 'wxpay', '红包', kb_spent=0)
#         choose_scarlett(996, 'wxpay', result['data']['payRequestId'], partner_id=pay.partner_id)
    if flag == 8:
#         result = pay.recharge(1, 'wxpay')
#         choose_scarlett(1, 'wxpay', result['data']['payRequestId'], partner_id=pay.partner_id)
#         pay.recharge(999999999, 'alipay')
#         pay.recharge_with_kb_negative(1, 'alipay', vou_key='消费')    #SYSTEM_ERROR
#         pay.recharge_with_kb_negative(1, 'alipay', vou_key='消费', currencySystem='COCOIN_ALLOWED')    #可币充值仅限渠道支付
        pay.recharge_with_kb_negative(1, 'wxpay', kb_spent=1)
    if flag == 9:
        # 银行卡支付
        


