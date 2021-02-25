#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/2/25 18:31
# comment:
import requests
from lib.common.algorithm.md5 import md5
from lib.common.utils.env import get_env_config
from lib.common_biz.sign import coda_pay_sign_string


def coda_pay(TotalPrice, PaymentType, MnoId, OrderId, ResultCode="0"):
    """
    {TxnId=6142429221971401254, Checksum=cc9281050d4ac0888b24b003f5f61186, TotalPrice=10000.00, PaymentType=1, MnoId=24, OrderId=ID202102250848423749T8JV1N847233, ResultCode=0}
    :param TotalPrice:
    :param PaymentType:

    253=codapay_7eleven, 1=codapay, 221=codapay_alfamart, 331=codapay_7chains, 332=codapay_linepay,
    226=codapay_indomaret, 227=codapay_gopay, 390=codapay_paytm, 391=codapay_upi, 251=codapay_store, 340=codapay_card,
    252=codapay_gcash}

    :param MnoId:

    {22=Indosat, 23=XL, 24=Telkomsel, 26=Tri Indonesia, 150=Zain (Bahrain), 131=Unitel, 132=Lao Telecom, 90=Globe,
    91=Smart/Sun, 70=DTAC, 71=AIS, 50=MAXIS, 72=CAT, 51=DiGi, 52=Celcom, 53=U Mobile, 160=Zain (Kuwait), 140=Etisalat,
    121=Smart Axiata, 122=Cellcard, 101=Telenor Myanmar, 102=Ooredoo, 103=MPT, 104=Mytel, 80=Taiwan Mobile,
    81=FarEasTone, 60=Dialog, 40=SingTel, 41=M1, 42=StarHub}

    :param OrderId:
    :param ResultCode:
    :return:
    """

    scarlett_data = {
        "TxnId": "6142429221971401254",
        "TotalPrice": TotalPrice,
        "PaymentType": PaymentType,
        "MnoId": MnoId,
        "OrderId": OrderId,
        "ResultCode": ResultCode,
        "Checksum": ""
    }
    # {"360":"1c3d4a652f744f340e7ad9471dbdcb5d","356":"95ec946be39a03944086430076bfef5d","608":"5657527817e99925747cbda5e53248a8",
    # "458":"bd781d681e3235f93ff1d7340f7a422b","764":"1c1566c01bf1538ee602cba31c70ec51","360_codapay_xl":"de47a25525e59c00ed8d6bddbd602c251",
    # "360_codapay_telkomsel":"b22585f8e2faa9cdee46a0afee02a12e1","360_codapay_tri":"7a792fe69b5333eecc7223475ce786791",
    # "360_codapay_smartfren":"5094dfe6b2f66d9874fdc4f1dc0f00261","360_codapay_indosat":"681fc7914e364a0ca21514921a9616291",
    # "764_codapay_dtac":"d07e95af7695870be6ffccd6f1e979b63","764_codapay_ais":"4cf10001f642acef41697461f6b95b663",
    # "608_codapay_globe":"82a48c16fd04f4221363d07a15c3c19b2","608_codapay_smart":"b8d30842761de43d501052ce4a797e3d2"}
    scarlett_data['Checksum'] = md5(coda_pay_sign_string(scarlett_data, "1c3d4a652f744f340e7ad9471dbdcb5d"), False)
    req = 'TxnId=6142429221971401254&' \
          'Checksum={}' \
          '&TotalPrice={}&' \
          'PaymentType={}&' \
          'MnoId={}&' \
          'OrderId={}&' \
          'ResultCode=0'.format(scarlett_data['Checksum'],TotalPrice, PaymentType, MnoId, OrderId)
    response = requests.get(get_env_config()['url']['pay_scarlet_out'] + "/opaycenter/codapaynotify?" + req)
    result = response.content
    print(result)


if __name__ == '__main__':
    coda_pay("1000.00", "390", "24", "PH202102251408112076075925774033")