#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

r=requests.get('http://www.baidu.com')
print(r.text)