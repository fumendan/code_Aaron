#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil

class disk():
    def allpart():
        disk_all={}
        allpart = psutil.disk_partitions()  # 全部分区列表
        for sdiskpart in allpart:
            disk_all[sdiskpart.device] = psutil.disk_usage(sdiskpart.device).total  # 通过sdiskpart.device获取的分区大小
        return disk_all
