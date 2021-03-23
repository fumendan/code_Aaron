#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core import manage
import requests

if __name__ == '__main__':
    server_info = manage.man()
    print('server_info:', server_info)
    # r = requests.post(url='http://127.0.0.1:8000/api/assets/', json=server_info)
    # print(r.text)
    # print(server_info)
