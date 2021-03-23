#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil

class cpu():
    def count():
        cpu_count={'count':psutil.cpu_count()}
        return cpu_count

    def status():
        cpu_status={'status':psutil.cpu_stats()}
        return cpu_status

    def times():
        cpu_times={'times':psutil.cpu_times()}
        return cpu_times
