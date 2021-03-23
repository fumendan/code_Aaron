#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import subprocess


host_name = subprocess.getoutput('hostname')

host_info = host_name[:]
print(host_info)
asset_api = 'http://127.0.0.1:8000/api/assets/'
requests.post(url=asset_api, data={'host_info': host_info})
