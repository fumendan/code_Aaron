#!/usr/bin/env python
# -*- coding:utf-8 -*-

from db import models


class GetResource(object):
    def __init__(self):
        self.inventory_date_dict = {}
        self.meta = {"_meta": {"hostvars": {}}}

        self.ig_queryset = models.InventoryGroups.objects.all()
        self.ih_queryset = models.InventoryHosts.objects.all()

    def get_inventory_groups(self):

        for ig_obj in self.ig_queryset:
            # 此组的组名
            prent_group_name = ig_obj.group_name

            # 先丁定义一个以此组名为 key 的空字典，之后用 update 的方法把其他键值对更新到此字典中
            self.inventory_date_dict[prent_group_name] = {}

            # 得到此组的变量
            vars_dict = {var.key: var.values for var in ig_obj.variableinfo_set.all() if var}
            if vars_dict:
                self.inventory_date_dict[prent_group_name].update({"vars": vars_dict})

            # 得到此组的全部子组组名
            child_list = [child.group_name for child in ig_obj.inventorygroups_set.all() if child]
            if child_list:
                # 把自己从子组列表中去除
                if prent_group_name in child_list:
                    child_list.remove(prent_group_name)

                # ["子组1","子组2", ...]
                self.inventory_date_dict[prent_group_name].update({"children": child_list})

            #  得到组的所有主机 ip
            hosts_ip_list = [host_obj.host.manage_ip for host_obj in ig_obj.inventoryhosts_set.all() if host_obj]

            if hosts_ip_list:
                val = self.inventory_date_dict[prent_group_name].get("vars")
                child = self.inventory_date_dict[prent_group_name].get("children")
                if any([val, child]):
                    self.inventory_date_dict[prent_group_name].update({"hosts": hosts_ip_list})
                else:
                    self.inventory_date_dict[prent_group_name] = hosts_ip_list
                    # {"组名": ['ip1','ip2']}

            # 最后处理一下空组，假如这个组没没有任何 key，则删除
            if not self.inventory_date_dict[prent_group_name]:
                self.inventory_date_dict.pop(prent_group_name)

        """
            "_meta" : {
           "hostvars" : {
              "moocow.example.com"     : { "asdf" : 1234 },
              "llama.example.com"      : { "asdf" : 5678 },
           }
        }


        """

    def get_all_host_var(self):
        """
        获取到所有主机的所有变量
        :return:  meta 字典
        """
        for ih in self.ih_queryset:
            tmp_dic = {var_obj.key: var_obj.values for var_obj in ih.variableinfo_set.all()}
            host = ih.host.manage_ip
            self.meta["_meta"]["hostvars"][host] = tmp_dic

    def get_resource(self):
        """
        这里是入口方法
        执行函数，整合数据
        :return:  resource 字典
        """
        self.get_inventory_groups()
        self.get_all_host_var()
        self.inventory_date_dict.update(self.meta)
        return self.inventory_date_dict

