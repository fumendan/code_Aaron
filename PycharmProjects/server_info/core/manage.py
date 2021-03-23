#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from conf import settings
import importlib


def man():
    server_info = {}
    for k, v in settings.menu_info.items():
        modpath, func = v.rsplit('.', maxsplit=1)
        mod_obj = importlib.import_module(modpath)
        if hasattr(mod_obj, k):
            server_info[k] = getattr(mod_obj, k)()
    return server_info
