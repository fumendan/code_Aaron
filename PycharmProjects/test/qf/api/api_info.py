#!/usr/bin/env python3
# coding=utf-8

from qf.lib import func_lib
# from qf.lib.decorator import start

# @start
def get_cpu_info():
    print('CPU count:',func_lib.cpu_count())
    # print(cpu_count)

def get_mem_info():
    print('Mem used(m):',func_lib.mem_size().used/1024/1024)