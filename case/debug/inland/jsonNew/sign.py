from lib.interface_biz.http.refactor.sign import SignPayGWClient, SignPayGWApi


if __name__ == '__main__':
    flag = 6    
    sign = SignPayGWClient() if flag in range(5) else SignPayGWApi()
    if flag == 1:
#         sign.sign_and_pay(1, 'alipay')
#         sign.query_sign_result()
#         sign.sign_and_pay(1, 'wxpay')
#         sign.query_sign_result()
        sign.sign_and_pay(9999999999, 'wxpay')      #SYSTEM_ERROR，超过int最大值
#         sign.sign_and_pay(2147483647, 'wxpay')    #core-wxpay异常：请求失败,请换其他支付方式
#         sign.query_sign_result()
#         sign.sign_and_pay(999999999, 'alipay')
#         sign.query_sign_result()
#         sign.sign_and_pay_negative(1, 'wxpay', processToken='', thirdPartId=0)   #
    if flag == 2:
        sign.sign_only('alipay')
#         sign.query_sign_result()
        sign.sign_only('wxpay')
#         sign.query_sign_result(pay_type='wxpay')
        sign.sign_only('alipay', 1)
        sign.query_sign_result()
        sign.sign_only('wxpay', 99999999)
        sign.query_sign_result(pay_type='wxpay')
    if flag == 3:
#         sign.sign_and_pay_negative(99999999999, 'wxpay')    #core-wxpay异常：“标价金额”字符串规则校验失败，字节数11，大于最大值10
#         sign.sign_and_pay_negative(0, 'wxpay')   #请求失败,请换其他支付方式
#         sign.sign_and_pay_negative(0, 'alipay', renewProductCode='')   #renewProductCode must not be empty
#         sign.sign_and_pay_negative(0, 'alipay', partnerCode='')   #partnerCode must not be empty
        sign.sign_and_pay_negative(1, 'alipay', signPartnerOrder=1)   #signPartnerOrder must not be empty
#         sign.sign_and_pay_negative(0, 'alipay', signPartnerOrder='')   #signPartnerOrder must not be empty
#         sign.sign_and_pay_negative(0, 'alipay', appPackage='')   #appPackage must not be empty
#         sign.sign_and_pay_negative(0, 'alipay', notifyUrl='')   #notifyUrl must not be empty
#         sign.sign_and_pay_negative(0, 'alipay', country='')   #country must not be empty
#         sign.sign_and_pay_negative(0, 'alipay', currency='')   #currency must not be empty
#         sign.sign_and_pay_negative(0, 'alipay', transType='1')   #报错信息有问题
#         sign.sign_and_pay_negative(payType='1')   #autoRenewMerchantInfo is empty
#         sign.sign_and_pay_negative(1, 'wxpay', processToken='')   #未报错，有问题
#         sign.sign_and_pay_negative(1, 'wxpay', subject='')   #参数异常
#         sign.sign_and_pay_negative(1, 'wxpay', desc='')   #参数异常
#         sign.sign_and_pay_negative('', 'alipay')   #参数异常
#         sign.sign_and_pay_negative(1, 'alipay', screenInfo='aaaaaaaaaa')   #未报错，有问题
    if flag == 4:
        sign.sign_only_negative('wxpay', processToken='')   #ssoId is emptyagreement_no, pay_type, amount
    
    if flag == 5:
        sign.unsign('20215417728171407557', 'alipay', '30926ef645fb4e828092a95a60c305ba')
        sign.unsign('20215417728171407557', 'alipay', '30926ef645fb4e828092a95a60c305ba')   #重复解约
    if flag == 6:
        sign.autorenew('20215417728171407557', 'alipay', 1)
#         sign.autorenew(1, 'alipay', 1)  #错误的renewProductCode、ssoid、agreementNo，签约信息校验失败
#         sign.autorenew('20215417728171407557', 'alipay', 1, ssoid=1)  #错误的renewProductCode、ssoid、agreementNo，签约信息校验失败
#         sign.autorenew('20215417728171407557', 'alipay', 1, renewProductCode=1)  #错误的renewProductCode、ssoid、agreementNo，签约信息校验失败