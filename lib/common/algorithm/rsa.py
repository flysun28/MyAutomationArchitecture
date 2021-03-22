#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:10
# comment:
import base64
import rsa as rsa_lib
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA


def rsa(original_str, key):
    """
    :param original_str:
    :param key: 私钥
    :return:
    """
    private_keyBytes = base64.b64decode(key)
    priKey = RSA.importKey(private_keyBytes)
    signer = PKCS1_v1_5.new(priKey)
    hash_obj = SHA.new(original_str.encode('utf-8') if isinstance(original_str, str) else original_str)
    sign = base64.b64encode(signer.sign(hash_obj))
    return sign


class _RSA():
    '''
    Unused
    '''    
    def __init__(self, pub_key, priv_key):
        self.pub_key = pub_key
        self.priv_key = priv_key
        print('RSA public key:', self.pub_key)
        
    def encrypt(self, original_str):
        # 生成公钥、私钥
    #     (pubkey, privkey) = rsa_lib.newkeys(512)
    #     print("公钥:\n%s\n私钥:\n:%s" % (pubkey, privkey))
        # 明文编码格式
        content = original_str.encode("utf-8") if isinstance(original_str, str) else original_str        
        # 公钥加密
        return rsa_lib.encrypt(content, self.pub_key)
     
    # rsa解密
    def decrypt(self, encrypted):
        # 私钥解密
        content = rsa_lib.decrypt(encrypted, self.priv_key)
        return content.decode("utf-8")
 
 
