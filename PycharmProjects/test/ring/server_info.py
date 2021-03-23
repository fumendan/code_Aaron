#!/usr/bin/env python3
#coding=utf-8

import psutil

def get_cpu_count():
    return psutil.cpu_count()

def show_cpu_info():
    count=get_cpu_count()
    cpu_info='''CPU count:{}'''
    print(cpu_info.format(count))

def get_mem():
    return psutil.virtual_memory()

def show_mem_total():
    total=get_mem().total/1024/1024//1024
    mem_info='''Memory total:%sG'''
    print(mem_info % total)

def show_mem_used():
    used=get_mem().used/1024/1024
    mem_info = '''Memory used:%sM'''
    print(mem_info % used)

if __name__=='__main__':
    show_cpu_info()
    show_mem_total()
    show_mem_used()

