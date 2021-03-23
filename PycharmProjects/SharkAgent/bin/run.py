#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import sys
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from src.Plugins import PluginMg
from library.util import check_hostname, api_auth


if __name__ == '__main__':
    pg_obj = PluginMg()
    host_dict = pg_obj.plugin_handler()

    # 更新主机名, 保障主机名是唯一的
    host_dict = check_hostname(host_dict)
    print('-->', host_dict)

    # 汇报数据
    # auth_info = api_auth()
    # print(auth_info)
    # response = requests.post(url='http://127.0.0.1:8000/api/asset.html', headers={'auth-api': auth_info}, json=host_dict)
    response = requests.post(url='http://127.0.0.1:8000/api/assets/', json=host_dict)
    print('response', response.text)
