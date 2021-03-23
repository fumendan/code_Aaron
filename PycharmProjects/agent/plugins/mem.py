#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil

class mem():
    def total():
        mem_total={'total':psutil.virtual_memory().total}
        return mem_total

    def used():
        mem_used={'used':psutil.virtual_memory().used}
        return mem_used

    def free():
        mem_free={'free':psutil.virtual_memory().free}
        return mem_free
