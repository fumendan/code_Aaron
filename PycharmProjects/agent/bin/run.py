#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import requests

BASEPATH=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASEPATH)

# from core import manage
#
# if __name__ == '__main__':
#     manage.man()

from core.main import main
if __name__ == '__main__':
    server_info=main()
    print(server_info)

    # response=requests.post(url='http://127.0.0.1:8000/api/assets/',json=server_info)
    # print(response.text)