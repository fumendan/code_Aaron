#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.db.models import F
from db import models


class TaskDataHandler(object):

    def __init__(self, cleaned_data):
        """
        :param cleaned_data: {'module_name': 7, 'remote_user': 1, 'module_type': 1, 'exec_args': 'ls /tmp', 'invent_hosts_id': ['6', '7']}

        """

        self.data_dict = cleaned_data
        self.ih_id = self.data_dict['invent_hosts_id']
        self.module_name_id = self.data_dict['module_name']
        self.module_type_id = self.data_dict['module_type']
        self.remote_user_id = self.data_dict['remote_user']
        """
        [{'manage_ip': '172.16.153.130','hostname':'gjzfapp1','port': 22, 'remote_user': 'root'},
             {'manage_ip': '172.16.153.131','hostname':'gjzfapp2','port': 22, 'remote_user': 'root'},
             ...]
             {"module_name": ''}
        """
    def to_int(slef,arg):
        if isinstance(arg, list):
            return [int(i) for i in arg]
        else:
            return [int(i) for i in [arg]]

    def get_data(self):
        # 根据 ih_id 进行夸表查询，获取到连接信息
        inventory_host_id = self.to_int(self.ih_id)
        remote_user_id = self.to_int(self.remote_user_id)
        con_qst = models.ConnectionInfo.objects.filter(host__id__in=inventory_host_id,  # 过滤主机 id
                                                       id__in=remote_user_id)  # 过滤远程用户 id

        # 取出字段和值
        con_qst_dic = con_qst.annotate(manage_ip=F("host__host__manage_ip"),  # 给超长字段起个别名
                                       host_name=F("host__host__hostname")
                                       ).values('manage_ip',
                                                'host_name',
                                                'remote_user',
                                                'password',
                                                'port')

        all_hosts_list = [item.get('manage_ip') for item in con_qst_dic]

        con_dic_list = list(con_qst_dic)
        con_dic_list.append({'select_hosts_list': all_hosts_list})

        module_name = models.ModuleInfo.objects.filter(id=int(self.module_name_id)  # 过滤
                                                       ).values_list('module_name').first()[0]

        return con_dic_list, module_name









