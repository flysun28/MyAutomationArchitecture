#!/usr/bin/env Python3
# -*- encoding:utf-8 *-*
# author:xy
# datetime:2021/1/19 23:07
# comment:
import base64
import rsa
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from common_biz.file_path import public_key_path


class Cipher:
    def __init__(self, original_str):
        """
        :param original_str: 加密内容
        """
        self.original_str = original_str

    def cipher(self):
        """
        公钥加密,使用Crypto.Cipher库
        :return:  加密之后的密文
        """
        # 获取公钥
        with open(public_key_path, 'rb') as public_key_file:
            key = public_key_file.read()
        public_key = RSA.importKey(key)
        # 分段加密
        pk = Cipher_pkcs1_v1_5.new(public_key)
        encrypt_text = []
        for i in range(0, len(self.original_str), 100):
            cont = self.original_str[i:i+100]
            encrypt_text.append(pk.encrypt(cont.encode()))
        cipher_text = b''.join(encrypt_text)
        result = base64.b64encode(cipher_text)
        return result.decode()

    def decrypt(self):
        """
        私钥进行解密
        :return:  解密之后的内容
        """
        msg = base64.b64decode(self.original_str)
        private_key = open('private.pem').read()
        rsa_key = RSA.importKey(private_key)
        cipher = PKCS1_v1_5.new(rsa_key)
        # 进行解密
        text = []
        for i in range(0, len(msg), 128):
            cont = msg[i:i+128]
            text.append(cipher.decrypt(cont,1))
        text = b''.join(text)
        return text.decode()

    def get_encrypt_data(self):
        """
        分段加密: 公钥加密,使用rsa库
        :return:
        """
        params = self.original_str.encode("utf-8")
        length = len(params)
        default_length = 117
        if length < default_length:
            return encrypt_data
        offset = 0
        params_lst = []
        while length - offset > 0:
            if length - offset > default_length:
                params_lst.append(encrypt_data(params[offset:offset + default_length]))
            else:
                params_lst.append(encrypt_data(params[offset:length - offset]))
            offset += default_length
        n = len(params_lst)
        c = 1
        res = params_lst[0]
        while c < n:
            res = res + params_lst[c]
            c += 1
        return res


def encrypt_data(original_str):
    """
    用公钥加密
    :param original_str:
    :return:
    """
    with open(public_key_path, 'rb') as public_key_file:
        p = public_key_file.read()
    pubkey = rsa.PublicKey.load_pkcs1(p)
    crypt_text = rsa.encrypt(original_str, pubkey)
    a = base64.b64encode(crypt_text)
    return a


if __name__ == '__main__':
    a = Cipher("1").cipher()