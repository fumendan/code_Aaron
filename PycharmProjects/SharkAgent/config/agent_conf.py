#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 方式二 定义获取主机信息的插件
PLUGINS_TEMPLATE = {
    'base_info': 'src.Plugins.base_info.BaseInfo',
    'motherboard': 'src.Plugins.motherboard.Motherboard',
    'cpu': 'src.Plugins.cpu.Cpu',
    'memory': 'src.Plugins.memory.Memory',
    'disk': 'src.Plugins.disk.Disk',
    'nic': 'src.Plugins.nic.Nic',
}


# 方式一 定义获取主机信息的命令类表
CMD_DICT = {
    'motherboard': "echo '主板'",
    'cpu': "echo 'cpu'",
    'memory': "echo '内存'",
    'disk': "echo '硬盘'",
    'nic': "echo ''网卡",
}
# CMD_DICT = {
#     'motherboard': "echo '主板'",
#     'cpu': "grep 'model name' /proc/cpuinfo | uniq;"
#            "grep 'physical id' /proc/cpuinfo | sort -u | wc -l;"
#            "grep 'processor'  /proc/cpuinfo  | wc -l",
#     'memory': "free -m",
#     'disk': "df ",
#     'nic': "echo ''网卡",
# }

#  向 CMDB 提交数据的 usl
REPORT_API = "http://127.0.0.1:8000/api/asset.html"

DEBUG = True
