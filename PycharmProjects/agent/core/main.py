#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib
from conf import settings

plugins_tmp=settings.PLUGINS_TMP

def main():
    for k,v in plugins_tmp.items():
        mod_name,cls_name=v.rsplit('.',maxsplit=1)
        info=importlib.import_module(mod_name)
        cls=getattr(info,cls_name)
        val=getattr(cls,'cmd')
        cpu_info={k:val()}
    return cpu_info
