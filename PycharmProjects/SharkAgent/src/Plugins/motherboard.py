#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from .basicplugin import BasicPlugin


class Motherboard(BasicPlugin):

    def cmd_handler(self, debug=True):
        """
        这里处理结果，返回格式化好的字典类型的数据
        :param debug:
        :return:
        """
        if debug:
            result = open('files/board.out', 'r', encoding='utf-8').read()
        else:
            result = self.run_cmd("sudo dmidecode -t1 2>/dev/null")
        return self.parse(result)

    def parse(self, content):

        result_dict = {}
        key_map = {
            'Manufacturer': 'manufacturer',
            'Product Name': 'model',
            'Serial Number': 'sn',
        }

        res_list = [line.strip() for line in content.split('\n')]
        item_dict = {item.split(':')[0]: item.split(':')[1] for item in res_list if len(item.split(':')) == 2}
        result_dict = {key_map[k]: v for k, v in item_dict.items() if k in key_map.keys()}


        # for item in content.split('\n'):
        #     row_data = item.strip().split(':')
        #     if len(row_data) == 2:
        #         if row_data[0] in key_map:
        #             result_dict[key_map[row_data[0]]] = row_data[1].strip() if row_data[1] else row_data[1]
        return result_dict
