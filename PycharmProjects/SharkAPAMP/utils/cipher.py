#!/usr/bin/env python
# -*- coding:utf-8 -*-
from cryptography.fernet import Fernet


class Crypto(object):
    def __init__(self):
        self.c_key = b'YrrndDCGiZjuYaIKtDq0bt1cNRqOMgtbcCGQBwtNwuo='
        # 生成带密钥的实例对象
        self.fernet_obj = Fernet(self.c_key)

    def encryption(self, text):
        # 调用实例对象的加密方法，对明文进行加密
        encrypted_text = self.fernet_obj.encrypt(text.encode('utf-8'))
        return encrypted_text.decode('utf-8')

    def decrypt(self, encrypted_text):
        decrypted_text = self.fernet_obj.decrypt(encrypted_text.encode('utf-8'))
        return decrypted_text.decode('utf-8')
