#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .basicplugin import BasicPlugin
from library import convert


class Memory(BasicPlugin):

    def cmd_handler(self, debug=True):
        if debug:
            memory_info = open('./files/memory.out', 'r', encoding='utf-8').read()
        else:
            memory_info = self.run_cmd("sudo dmidecode  -q -t 17 2>/dev/null")
        return self.parse(memory_info)

    def parse(self, content):
        """
        解析shell命令返回结果
        :param content: shell 命令结果
        :return:解析后的结果
        """
        ram_dict = {}
        key_map = {
            'Size': 'capacity',
            'Locator': 'slot',
            'Type': 'model',
            'Speed': 'speed',
            'Manufacturer': 'manufacturer',
            'Serial Number': 'sn',

        }
        devices = content.split('Memory Device')
        for item in devices:
            item = item.strip()
            if not item:
                continue
            if item.startswith('#'):
                continue
            segment = {}
            lines = item.split('\n\t')
            for line in lines:
                if not line.strip():
                    continue
                if len(line.split(':')):
                    key, value = line.split(':')
                else:
                    key = line.split(':')[0]
                    value = ""
                if key in key_map:
                    if key == 'Size':
                        segment[key_map['Size']] = convert.convert_mb_to_gb(value, 0)
                    else:
                        segment[key_map[key.strip()]] = value.strip()

            ram_dict[segment['slot']] = segment

        return ram_dict