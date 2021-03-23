# import os, sys
# from SharkAPAMP import settings
# from ansible import constants
# from collections import namedtuple
# from ansible.parsing.dataloader import DataLoader
# from ansible.vars.manager import VariableManager
# from ansible.inventory.manager import InventoryManager
# from ansible.playbook.play import Play
# from ansible.executor.playbook_executor import PlaybookExecutor
# from ansible.executor.task_queue_manager import TaskQueueManager
# from ansible.plugins.callback import CallbackBase
# from ansible.inventory.host import Host, Group
# PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath('__file__'))))
# sys.path.insert(0, PROJECT_ROOT)
# os.environ["DJANGO_SETTINGS_MODULE"] = 'SharkAPAMP.settings'
# import django
# django.setup()

# from db import models

# loader = DataLoader()
# inventory = InventoryManager(loader=loader, sources='%s/conf/hostlist' % settings.BASE_DIR)
# inventory_date_dict ={
#     "组名": {
#         "hosts": ["ip1", "ip2"],
#         "vars": {
#             "k1": 'v1'
#         },
#         "child": ['子组1','子组2']
#     },
#     "webservers": ["host2.example.com", "host3.example.com"],
#     "atlanta": {
#         "hosts": ["host1.example.com", "host4.example.com", "host5.example.com"],
#         "vars": {
#             "b": False
#         },
#         "children": ["marietta", "5points"]
#     },
#     "marietta": ["host6.example.com"],
#     "5points": ["host7.example.com"]
# }


# class GetResource(object):
#     def __init__(self):
#         self.inventory_date_dict = {}
#         self.all_group_name_list = []
#         self.meta = {"_meta": {"hostvars": {}}}
#
#         self.ig_queryset = models.InventoryGroups.objects.all()
#         self.ih_queryset = models.InventoryHosts.objects.all()
#
#     def get_inventory_groups(self):
#
#         for ig_obj in self.ig_queryset:
#             # 组的组名
#             prent_group_name = ig_obj.group_name
#             # 将组名添加到列表里
#             self.all_group_name_list.append(prent_group_name)
#
#             self.inventory_date_dict[prent_group_name] = {}
#
#             # 得到此组的变量
#             vars_dict = {var.key: var.values for var in ig_obj.variableinfo_set.all() if var}
#             if vars_dict:
#                 self.inventory_date_dict[prent_group_name].update({"vars": vars_dict})
#
#             # 得到此组的全部子组组名
#             child_list = [child.group_name for child in ig_obj.inventorygroups_set.all() if child]
#             if child_list:
#                 # 把自己从子组列表中去除
#                 if prent_group_name in child_list:
#                     child_list.remove(prent_group_name)
#
#                 # ["子组1","子组2", ...]
#                 self.inventory_date_dict[prent_group_name].update({"children": child_list})
#
#             #  得到组的所有主机 ip
#             hosts_ip_list = [host_obj.host.manage_ip for host_obj in ig_obj.inventoryhosts_set.all() if host_obj]
#
#             if hosts_ip_list:
#                 val = self.inventory_date_dict[prent_group_name].get("vars")
#                 child = self.inventory_date_dict[prent_group_name].get("children")
#                 if any([val, child]):
#                     self.inventory_date_dict[prent_group_name].update({"hosts": hosts_ip_list})
#                 else:
#                     self.inventory_date_dict[prent_group_name] = hosts_ip_list
#                     # {"组名": ['ip1','ip2']}
#
#             # 最后处理一下空组，假如这个组没没有任何 key，则删除
#             if not self.inventory_date_dict[prent_group_name]:
#                 self.inventory_date_dict.pop(prent_group_name)
#
#         # 将主机组列表添加到字典中
#         self.inventory_date_dict["all_groups_name"] = self.all_group_name_list
#
#
#         """
#             "_meta" : {
#            "hostvars" : {
#               "moocow.example.com"     : { "asdf" : 1234 },
#               "llama.example.com"      : { "asdf" : 5678 },
#            }
#         }
#
#
#         """
#
#     def get_all_host_var(self):
#         """
#         获取到所有主机的所有变量
#         :return:  meta 字典
#         """
#         for ih in self.ih_queryset:
#             tmp_dic = {var_obj.key: var_obj.values for var_obj in ih.variableinfo_set.all()}
#             host = ih.host.manage_ip
#             self.meta["_meta"]["hostvars"][host] = tmp_dic
#
#     def get_resource(self):
#         """
#         执行函数，整合数据
#         :return:  resource 字典
#         """
#         self.get_inventory_groups()
#         self.get_all_host_var()
#         self.inventory_date_dict.update(self.meta)
#         return self.inventory_date_dict


class Person(object):
    city = '北京'               # 类属性，也称为静态字段

    def __init__(self, name):
        self.name = name       # 实例属性, 有时候叫普通字段

    def instance_func(self):
        """ 定义普通方法，至少有一个self参数 """
        print("{}调用实例方法".format(self))

    @classmethod
    def class_func(cls):
        """ 定义类方法，至少有一个cls参数 """

        print('{}调用类方法'.format(cls))

    @staticmethod
    def static_func():
        """ 定义静态方法 ，无需默认参数"""

        print('调用静态方法')

# 调用普通方法
print("-" * 50)
print("对象可以调用的方法")
obj = Person("QF")
obj.instance_func()
obj.class_func()
obj.static_func()
print("-" * 50)

# 类可以调用的方法
print("-" * 50)
Person.class_func()
Person.static_func()
Person.instance_func("y")
print("-" * 50)



