'''
Created on 2021年3月16日
@author: 80319739
'''
import os
import base64
import jnius_config
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from lib.common.file_operation.xml_operation import MvnSettingXML
from lib.config.path import case_dir


class AES_CBC():
    mode = AES.MODE_CBC

    def __init__(self, priv_key, iv):
        self.priv_key = priv_key
        self.iv = iv
        print('AES_CBC aes私钥: %s\tiv: %s' %(self.priv_key, self.iv))
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
        cipher_text = cryptos.encrypt(text)
        # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
        self.enc_text = b2a_hex(cipher_text)
        return self.enc_text

    # 解密后，去掉补足的空格用strip()去掉
    def decrypt(self, enc_text=None):
        key = self.priv_key.encode('utf-8') if isinstance(self.priv_key, str) else self.priv_key
        enc_text = enc_text if enc_text else self.enc_text
        cryptos = AES.new(key, self.mode, self.iv)  # Data must be padded to 16 byte boundary in CBC mode
        try:
            plain_text = cryptos.decrypt(a2b_hex(enc_text))
        except:
            plain_text = cryptos.decrypt(enc_text)
        return bytes.decode(plain_text).rstrip('\0')

    def encrypt_and_base64(self, text):
        self.encrypt(text)
        print('aes加密之后：', self.enc_text)
        res = base64.b64encode(self.enc_text)
        print('base64加密之后：', res)
        return res


class AES_CTR():
    mode = AES.MODE_CTR


class AES4J_MultiJars():
#     mvn_repo_root = MvnSettingXML().local_repo
#     jars = [
#         mvn_repo_root + '/org/slf4j/slf4j-log4j12/2.0.0-alpha1/slf4j-log4j12-2.0.0-alpha1.jar',
#         mvn_repo_root + '/org/slf4j/slf4j-api/2.0.0-alpha1/slf4j-api-2.0.0-alpha1.jar',
#         mvn_repo_root + '/log4j/log4j/1.2.17/log4j-1.2.17.jar',
#         mvn_repo_root + '/commons-codec/commons-codec/1.11/commons-codec-1.11.jar',
#         mvn_repo_root + '/org/apache/commons/commons-lang3/3.8.1/commons-lang3-3.8.1.jar',
#         os.path.join(case_dir, 'src', 'jar', 'common-util-4.1.2-RELEASE.jar')
#     ]
#     jar_pathes = type(jars)(map(lambda p: p.strip(os.sep).replace('/', os.sep), jars))

    def __init__(self, priv_key, iv, version):
        self.priv_key = priv_key
        self.iv = iv
        self.version = version  #'X-Protocol-Ver'
        print('AES4J aes私钥: %s\tiv: %s' %(self.priv_key, self.iv))
        self.enc_text = None
        self.args = ()
        self.get_java_class()

    def get_java_class(self):
        jar_dir = os.path.join(case_dir, 'src', 'jar')
        jar_pathes = []
        for jar in os.listdir(jar_dir):
            jar_pathes.append(os.path.join(jar_dir, jar))
        for p in jar_pathes:
            assert os.path.exists(p), p
        jnius_config.set_classpath('.', *jar_pathes)
        '''
        autoclass必须在set_classpath之后导入，否则会报VM is already running, can't set classpath/options
        '''
        from jnius import autoclass
        self.AESUtil = autoclass('com.oppo.usercenter.common.util.security.AESUtil')
        self.Base64 = autoclass('org.apache.commons.codec.binary.Base64')

    def encrypt(self, text):
        self.args += text, self.priv_key
        if self.version == '2.0':
            self.args += 'CTR',
        elif self.version == '3.0':
            self.args += self.iv,
        self.enc_text = self.AESUtil.aesEncryptWithPassKey(*self.args)
#         print('aes加密之后：', self.enc_text)
        self.args = ()
        return self.enc_text

    def decrypt(self, enc_text=None):
        enc_text = self.enc_text if enc_text is None else enc_text
        return self.AESUtil.aesDecryptWithPassKey(enc_text, self.priv_key, self.iv)


class AES4J():

    def __init__(self, priv_key, iv, version):
        self.priv_key = priv_key
        self.iv = iv
        self.version = version  #'X-Protocol-Ver'
        print('AES4J aes私钥: %s\tiv: %s' %(self.priv_key, self.iv))
        self.enc_text = None
        self.args = ()
        self.get_java_class()

    def get_java_class(self):
        jar_dir = os.path.join(case_dir, 'src', 'jar')
        jnius_config.set_classpath('.', os.path.join(jar_dir, 'aes.jar'))
        '''
        autoclass必须在set_classpath之后导入，否则会报VM is already running, can't set classpath/options
        '''
        from jnius import autoclass
        self.AESUtil = autoclass('AESUtil')

    def encrypt(self, text):
        self.args += text, self.priv_key
        if self.version == '2.0':
            self.args += 'CTR',
        elif self.version == '3.0':
            self.args += self.iv,
        self.enc_text = self.AESUtil.Encrypt(*self.args)
#         print('aes加密之后：', self.enc_text)
        self.args = ()
        return self.enc_text

    def decrypt(self, enc_text=None):
        enc_text = self.enc_text if enc_text is None else enc_text
        return self.AESUtil.Decrypt(enc_text, self.priv_key, self.iv)

