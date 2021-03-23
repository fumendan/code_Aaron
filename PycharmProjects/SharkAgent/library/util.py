#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import time
import hashlib
from config.agent_conf import BASE_DIR
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


def check_hostname(host_dict):
    file_path = os.path.join(BASE_DIR, 'config', 'voucher')
    report_name = host_dict['base_info']['data']['hostname']
    with open(file_path, 'r') as f:
        host_name = f.read()

    # 假如没有获取到主机名，说明是第一次汇报资产信息，把主机名存档
    if not host_name:
        with open(file_path, 'w') as f:
            f.write(report_name)
    # 获取到主机名，说明不是第一次汇报了
    else:
        # 假如汇报的资产信息中的主机名不和存档的一样，需要遵循主机名为唯一标识的原则，
        # 更新汇报的资产信息中的主机名为存档的主机名
        if host_name != host_dict['base_info']['data']['hostname']:
            host_dict['base_info']['data']['hostname'] = host_name
    return host_dict


def md5_handler(arg):
    hs = hashlib.md5()
    hs.update(arg.encode('utf-8'))
    return hs.hexdigest()


def api_auth():
    key = "900qerjl;jkq_()kljldaf"
    ctime_str = str(time.time())
    md5_str = md5_handler("{}|{}".format(key, ctime_str))
    auth_info = "{}|{}".format(md5_str, ctime_str)  # 84f7d4c3a39b05a9fdf155f7bb181d78|时间戳
    return auth_info


