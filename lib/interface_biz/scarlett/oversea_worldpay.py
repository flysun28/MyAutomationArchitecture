#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/25 16:58
# comment: 未调通
import requests
from lib.common.utils.env import get_env_config


def world_pay():
    head={"Content-Type":"text/xml; charset=UTF-8", 'Connection': 'close'}
    world_pay_xml = '<?xml version="1.0" encoding="UTF-8"?>' \
                    '<!DOCTYPE paymentService PUBLIC "-//WorldPay//DTD WorldPay PaymentService v1//EN"' \
                    '"http://dtd.worldpay.com/paymentService_v1.dtd">' \
                    '<paymentService version="1.4" merchantCode="OPPOTEST"><notify><orderStatusEvent orderCode="VN20210225085402IK8EM4L1X2284123">' \
                    '<payment><paymentMethod>VISA-SSL</paymentMethod><paymentMethodDetail><card number="4444********1111" type="creditcard"><expiryDate><date month="12" year="2021"/></expiryDate></card></paymentMethodDetail><amount value="2000" currencyCode="VND" exponent="0" debitCreditIndicator="credit"/><lastEvent>AUTHORISED</lastEvent><CVCResultCode description="NOT SENT TO ACQUIRER"/><AVSResultCode description="NOT SUPPLIED BY SHOPPER"/><AAVAddressResultCode description="UNKNOWN"/><AAVPostcodeResultCode description="UNKNOWN"/><AAVCardholderNameResultCode description="UNKNOWN"/><AAVTelephoneResultCode description="UNKNOWN"/><AAVEmailResultCode description="UNKNOWN"/><cardHolderName><![CDATA[Xy]]></cardHolderName><issuerCountryCode>N/A</issuerCountryCode><balance accountType="IN_PROCESS_AUTHORISED"><amount value="2000" currencyCode="VND" exponent="0" debitCreditIndicator="credit"/></balance><riskScore value="1"/></payment>' \
                    '<journal journalType="AUTHORISED">' \
                    '<bookingDate><date dayOfMonth="25" month="02" year="2021"/></bookingDate><accountTx accountType="IN_PROCESS_AUTHORISED" batchId="205"><amount value="2000" currencyCode="VND" exponent="0" debitCreditIndicator="credit"/></accountTx></journal>' \
                    '</orderStatusEvent></notify></paymentService>'
    response = requests.post(get_env_config()['url']['pay_scarlet_out'] + "/opaycenter/worldpaynotify",
                             data=world_pay_xml, headers=head)
    result = response.content
    print(result)


if __name__ == '__main__':
    world_pay()