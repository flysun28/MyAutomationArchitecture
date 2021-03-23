'''
Created on 2021年3月16日
@author: 80319739
'''

import base64
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class AES_CBC():
    mode = AES.MODE_CTR
    
    def __init__(self, priv_key, iv):
        self.priv_key = priv_key
        self.iv = iv
        self.enc_text = None
    
    # 如果text不足16位的倍数就用空格补足为16位
    def add_to_16(self, text):
        if len(text.encode('utf-8')) % 16:
            add = 16 - (len(text.encode('utf-8')) % 16)
        else:
            add = 0
        text = text + ('\0' * add)
        return text.encode('utf-8')
    
    # 加密函数
    def encrypt(self, text):
        b_key = self.priv_key.encode('utf-8') if isinstance(self.priv_key, str) else self.priv_key
        text = self.add_to_16(text)
        cryptos = AES.new(b_key, self.mode, self.iv)
        cipher_text = cryptos.encrypt(text.encode('utf-8'))
        # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
        self.enc_text = b2a_hex(cipher_text)
        return self.enc_text
    
    # 解密后，去掉补足的空格用strip()去掉
    def decrypt(self, enc_text=None):
        key = self.priv_key.encode('utf-8') if isinstance(self.priv_key, str) else self.priv_key
        enc_text = enc_text if enc_text else self.enc_text
#         cryptos = AES.new(key, self.mode, self.iv)  # Data must be padded to 16 byte boundary in CBC mode
        cryptos = AES.new(key, self.mode)
        try:
            plain_text = cryptos.decrypt(a2b_hex(enc_text))
        except:
            plain_text = cryptos.decrypt(enc_text)
#         return plain_text
        return plain_text.decode()
        return bytes.decode(plain_text).rstrip('\0')
    
    def encrypt_and_base64(self, text):
        self.encrypt(text)
        print('aes加密之后：', self.enc_text)
        res = base64.b64encode(self.enc_text)
        print('base64加密之后：', res)
        return res


class AES_CTR():
    mode = AES.MODE_CTR

