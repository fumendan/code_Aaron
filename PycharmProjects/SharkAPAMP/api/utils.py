#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import hashlib
from django.shortcuts import HttpResponse
from django.core.cache import cache
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


def md5_handler(arg):
    hs = hashlib.md5()
    hs.update(arg.encode('utf-8'))
    return hs.hexdigest()


def api_auth(func):
    def inner(request, *args, **kwargs):
        key = "900qerjl;jkq_()kljldaf"

        # 获取服务器的当前时间
        server_float_ctime = time.time()

        # 获取客户端发过来的认证信息
        auth_info = request.META.get('HTTP_AUTH_API')  # 84f7d4c3a39b05a9fdf155f7bb181d78|时间戳

        # 对认证信息进行处理
        client_md5_str, client_ctime_str = auth_info.rsplit('|', maxsplit=1)
        client_float_ctime = float(client_ctime_str)

        # 判断是否是在 10 秒之内的认证信息
        if (client_float_ctime + 30) <= server_float_ctime:
            return HttpResponse('超时，认证失败')

        # 验证认证信息是否被篡改：
        server_md5_str = md5_handler("{}|{}".format(key, client_ctime_str))
        if client_md5_str != server_md5_str:
            return HttpResponse('认证信息不符，认证失败')

        # 验证是否是第一次
        if cache.get(client_md5_str):
            return HttpResponse('认证信息已认证过了，认证失败')

        # 假如都通过了以上的所有验证，认证信息通过，就把认证信息添加到 Redis 中
        cache.set(client_md5_str, client_float_ctime, timeout=30)
        return func(request, *args, **kwargs)

    return inner