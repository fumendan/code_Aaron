#!/usr/bin/env python3
#author:murongjin

import platform
import psutil

def getCPU():
    print("操作系统：",'\t',platform.uname().system,platform.uname().release)
    print("系统版本：",'\t',platform.uname().version)
    print("CPU架构：",'\t',platform.uname().machine)
    print("CPU信息：",'\t',platform.uname().processor)

def getSYS():
    print("计算机名：",'\t',platform.uname().node)
    print("IP地址：")
    ipDic={}
    netDic=psutil.net_if_addrs()
    for k in netDic:
        ipDic[k]={}
        for snic in netDic[k]:
            if snic.family.name == 'AF_INET':
                ipDic[k]['IPaddr']=snic.address
                ipDic[k]['netmask'] = snic.netmask
            if snic.family.name == 'AF_LINK':
                ipDic[k]['MACaddr'] = snic.address
    for k in ipDic:
        print('\t',k,':')
        for x in ipDic[k]:
            print('\t','\t',x,'\t',ipDic[k][x])

if __name__ == '__main__':
    getCPU()
    print("+"*50)
    getSYS()
