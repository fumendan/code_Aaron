#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import psutil

'''
1.cpu核心数
2.内存容量
3.硬盘分区，和每个分区的容量
4.网卡名，ip，netmask
'''


def cpu():
    cpu_count = psutil.cpu_count(logical=False)  # 物理核心数
    cpu_lgc_count = psutil.cpu_count()  # 逻辑核心数
    cpuinfo = {'cpu_count': cpu_count, 'cpu_lgc_count': cpu_lgc_count}
    return cpuinfo


def mem():
    total = psutil.virtual_memory().total  # 内存总数
    used = psutil.virtual_memory().used  # 使用内存
    free = psutil.virtual_memory().free  # 空闲内存
    meminfo = {'total': total, 'used': used, 'free': free}
    return meminfo


def disk():
    diskinfo = {}
    allpart = psutil.disk_partitions()  # 全部分区列表
    for sdiskpart in allpart:
        diskinfo[sdiskpart.device] = psutil.disk_usage(sdiskpart.device).total  # 通过sdiskpart.device获取的分区大小
    return diskinfo


def nics():
    import socket
    nicsinfo = {}
    for nics, snic_list in psutil.net_if_addrs().items():  # 遍历网卡设备字典,key为设备名，value为snic列表
        if nics != 'lo':
            nicsinfo[nics] = {}
            for snic in snic_list:  # 便利snic列表
                if snic.family == socket.AF_INET:  # 过滤IPv4
                    nicsinfo[nics]['ip'] = snic.address
                else:
                    nicsinfo[nics]['ip'] = ''
                if snic.family == socket.AF_PACKET:  # 过滤mac
                    nicsinfo[nics]['mac'] = snic.address
                else:
                    nicsinfo[nics]['mac'] = ''
    return nicsinfo
