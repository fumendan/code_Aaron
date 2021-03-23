#!/usr/bin/env python3
# coding=utf-8

from qf.api import api_info
from qf.lib.decorator import start

@start
def man():
    api_info.get_cpu_info()
    api_info.get_mem_info()


if __name__ == '__main__':
    man()
