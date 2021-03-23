#!/usr/bin/env python3
# coding=utf-8

import psutil

def cpu_count():
    return psutil.cpu_count()

def mem_size():
    return psutil.virtual_memory()