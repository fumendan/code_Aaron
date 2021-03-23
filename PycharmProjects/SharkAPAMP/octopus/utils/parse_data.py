#!/usr/bin/env python
# -*- coding:utf-8 -*-

# # 单独运行此文件时，请打开以下注释
import os, sys

# PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath('__file__'))))
# # print(PROJECT_ROOT)
# sys.path.insert(0, PROJECT_ROOT)
# os.environ["DJANGO_SETTINGS_MODULE"] = 'SharkAPAMP.settings'
# import django
# django.setup()
# 单独运行此文件环境变化设置完毕

import traceback
from datetime import datetime
from ansible import constants
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.inventory.host import Host, Group
from SharkAPAMP.settings import BASE_DIR, TASK_STATUS_CODE
from octopus.utils.cmdb_resource import GetResource
from SharkAPAMP.settings import INVENTORY_FILE

"""
示例数据：
{'_meta': {'hostvars': {'172.16.153.130': {'key': 'gjzfap1','server_key': 'server'},
                        '172.16.153.131': {'key': 'gjzfap2', 'server_key': 'server'},
                        '172.16.153.132': {'key': 'argap1', 'server_key': 'server'},
                        '172.16.153.133': {'key': 'argap2', 'server_key': 'server'},
                        '172.16.153.134': {'key': 'amonap1', 'server_key': 'server'},
                        '172.16.153.135': {'key': 'yargap1', 'server_key': 'server'}}},
   
 'all': {'children': ['gjzf', 'qudao']},
   
 'gjzf': {'children': ['gjzf_child1', 'gjzf_chid2'],
          'hosts': ['172.16.153.130', '172.16.153.131'],
          'vars': {'group_name': 'gjzf', 'key': 'gjzf_group'}},
          
 'gjzf_chid2': ['172.16.153.135'],
 
 'gjzf_child1': {'children': ['gjzf_child1_1'],
                 'hosts': ['172.16.153.134'],
                 'vars': {'key': 'gjzf_child1'}},
 'qudao': {'children': ['hf_group'],
           'hosts': ['172.16.153.132', '172.16.153.133']}}
"""


class DynamicInventory(object):
    def __init__(self):
        self.inventory_file = INVENTORY_FILE
        # 获取到 cmdb 的资源数据
        self.resource_handler = GetResource()
        self.__resource = self.resource_handler.get_resource()

        # 初始化资源库
        self.loader = DataLoader()
        self.inventory = InventoryManager(
            loader=self.loader,  # 用于加载和处理 json、yaml 文件的数据管理器
            sources=[self.inventory_file]  # 是一个或者多个文件。 相当于 /etc/ansible/inventory.py
        )
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

        # 首先初始化所有主机的变量
        self.hosts_vars = self.__resource.pop('_meta')
        # 调用实例方法(编号 D01)
        self.set_hosts_vars(self.hosts_vars)

        # 为了显而易见，我在此调用了这个类的实例方法，并且把 self.resource 作为参数传入这个方法中进行处理。
        # 这是这个类的入口方法
        # 第一步，调用实例方法(编号 D05)
        self.run_parser(self.resource)

    def set_hosts_vars(self, vars_dict):
        # 编号 D01
        if isinstance(vars_dict, dict):
            for h, v in self.hosts_vars['hostvars'].items():
                if all([isinstance(v, dict), v]):
                    # 创建主机对象
                    h_obj = Host(h)
                    for key, val in v.items():
                        self.variable_manager.set_host_variable(host=h_obj, varname=key, value=val)

    def add_host_to_group(self, hosts_list, group_name):
        # 编号 D02
        '''添加主机到主机组里'''
        if isinstance(hosts_list, list):
            hosts_list = hosts_list
        else:
            # 用于子类添加单个主机到资源库
            hosts_list = [hosts_list]

        for host_name_or_ip in hosts_list:
            self.inventory.add_host(host=host_name_or_ip, group=group_name)

    @staticmethod
    def set_gorup_vars(vars_dict, group_obj):
        # 编号 D03
        '''设置组变量'''
        if isinstance(vars_dict, dict):
            [group_obj.set_variable(k, v) for k, v in vars_dict.items()]

    @staticmethod
    def set_child_group(children_group_list, parent_group_obj):
        # 编号 D04
        '''设置子组'''
        [parent_group_obj.add_child_group(Group(children_group)) for children_group in children_group_list]

    def run_parser(self, resource):
        # 编号 D05
        for group_name, _item in resource.items():

            # 第二步，ansible inventory 的添加组方法, 把组添加到 Ansible 的资源库中
            self.inventory.add_group(group_name)
            current_group_obj = Group(group_name)
            if isinstance(_item, dict):
                if 'hosts' in _item.keys():
                    '''向目前的组，添加主机组成员'''
                    hosts_list = _item['hosts']
                    # 第三步，调用这个类的实例方法（编号 D02）
                    self.add_host_to_group(hosts_list, group_name)

                if 'vars' in _item.keys():
                    '''设置组变量'''
                    group_vars = _item['vars']
                    # 第四步， 获取到变量信息后，调用这个类的实例方法(编号 D03)
                    self.set_gorup_vars(vars_dict=group_vars, group_obj=current_group_obj)

                if "children" in _item.keys():
                    '''设置子组'''
                    children_list = _item["children"]
                    # 第五步，获取到这个组的子组数据后，调用实例方法(编号 D04)
                    self.set_child_group(children_list, current_group_obj)
                    # print(current_group_obj.child_groups)

            elif isinstance(_item, list):
                # 第六部，判断只有主机列表的组，并调用实例方法(编号 D02)
                hosts_list = _item
                self.add_host_to_group(hosts_list, group_name)

            else:
                print("添加了一个空组")

    def get_inventory_detail(self):
        # print(self.inventory.hosts)
        print(self.inventory.get_groups_dict())
        # print(self.variable_manager.get_vars())
        #
        # print(self.inventory.groups)
        # print(self.variable_manager.get_vars(host=self.inventory.get_host('172.16.153.130')))
        # return self.inventory.get_groups_dict()
        return self.inventory.hosts
    @property
    def resource(self):
        return self.__resource


if __name__ == '__main__':
    p = DynamicInventory()

    host_dict = p.get_inventory_detail()
    print(type(host_dict))
    print(p.resource)

