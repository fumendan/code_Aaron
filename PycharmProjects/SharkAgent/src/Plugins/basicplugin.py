#!/usr/bin/env python
# -*- coding:utf-8 -*-
from config import agent_conf


class BasicPlugin(object):
    def __init__(self, host_list=None):
        self.host_list = host_list

    def run_cmd(self, cmd_str=''):
        import subprocess
        res_status, res_info = subprocess.getstatusoutput(cmd_str)

        return res_info
