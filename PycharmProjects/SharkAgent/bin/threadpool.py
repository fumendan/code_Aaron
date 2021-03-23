#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def task(arg1, arg2):
    print(arg1, arg2)
    time.sleep(1)


thread_pool = ThreadPoolExecutor(20)

# for i in range(200):
#     thread_pool.submit(task, i, i,)


process_pool = ProcessPoolExecutor(10)

for i in range(200):
    process_pool.submit(task, i, i)
