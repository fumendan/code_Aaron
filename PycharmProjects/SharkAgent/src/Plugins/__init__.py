#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback
import importlib
from config import agent_conf


class PluginMg(object):
    def __init__(self, host=None):
        self.plugin = agent_conf.PLUGINS_TEMPLATE
        self.debug = agent_conf.DEBUG
        self.host = host
        self.host_info = {}

    def plugin_handler(self):
        
        """
        循环插件，执行每个插件的实例方法
        :return: 主机信息，字典类型
        """
        for k, v in self.plugin.items():
            # 'cpu': 'src.Plugins.cpu.Cpu'
            info = {'status': True, 'data': None, 'message': None}
                # 命令状态        具体的数据         附加信息
            try:
                # 从右边以 . 为分隔符
                module_path, cls_str = v.rsplit('.', maxsplit=1)

                # 利用反射导入，得到模块的对象
                module_obj = importlib.import_module(module_path)

                # 得到模块中的类对象
                cls_name_obj = getattr(module_obj, cls_str)
                obj = cls_name_obj()

                # 执行每个实例对象的 cmd_handler 方法，并返回对应的信息
                result = obj.cmd_handler(self.debug)

                info['data'] = result
            except Exception:
                info['status'] = False
                info['message'] = traceback.format_exc()
                print(traceback.format_exc())
            self.host_info[k] = info
        return self.host_info
