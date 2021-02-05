#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:10
# comment:
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


def rsa(original_str, key):
    """
    :param original_str:
    :param key:
    :return:
    """
    private_keyBytes = base64.b64decode(key)
    priKey = RSA.importKey(private_keyBytes)
    signer = PKCS1_v1_5.new(priKey)
    hash_obj = SHA.new(original_str.encode('utf-8'))
    sign = base64.b64encode(signer.sign(hash_obj))
    return sign
