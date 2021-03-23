#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback
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




class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in
    一个用于演示从执行任务的结果中， 进行处理的 回调 插件示例
    If you want to collect all results into a single object for processing at
    如果希望在执行结束时，将所有结果收集到单个对象中进行处理，
    the end of the execution,
    look into utilizing the ``json`` callback plugin or writing your own custom callback plugin
    那么应用去看看如何使用 “JSON” 回调插件或者编写自己的自定义回调插件
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result._result

    def v2_runner_on_ok(self, result,  *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result,  *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class PlayBookResultsCollector(CallbackBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.task_ok[result._host.get_name()]  = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.task_failed[result._host.get_name()] = result

    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        self.task_ok[result._host.get_name()]  = result

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for host in hosts:
            t = stats.summarize(host)
            self.task_status[host] = {
                                       "ok": t["ok"],
                                       "changed": t["changed"],
                                       "unreachable": t["unreachable"],
                                       "skipped": t["skipped"],
                                       "failed": t["failures"]
                                   }


class MyOptions(object):
    def __init__(self, *args, **kwargs):
        self.inintal_data()

    def inintal_data(self, **kwargs):
        # 通过一个命名元组，来设置需要的参数
        Options = namedtuple("Options",
                             ["connection","module_path", "forks", "timeout", "ask_pass",
                              "become", "become_method", "become_user",
                              "listhosts", "listtasks", "listtags",
                              "check", "syntax", "diff"])

        # Options 的参数都是全局的参数
        self.options = Options(connection="smart",     # 表示远程执行
                          module_path=None,       # 模块路径
                          forks=10,               # 并发执行10个线程
                          timeout=10,             # 任务超时时间
                          ask_pass=False,         # 是否出现：输入密码的提示

                          become=None,            # 是否升级权限
                          become_method=None,     # 设置特权升级方法。默认值是sudo，其他选项su，pbrun，pfexec，doas，ksu：
                          become_user=None,       # 升级为谁


                          listhosts=False,
                          listtasks=False,
                          listtags=False,

                          check=False,
                          syntax=False,
                          diff=True)


class Run(MyOptions):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置一个密码对象，字典类型, key 可以自定义, 这个是必须参数，但是可以为空
        # passwords = dict(vault_pass="upsa/upsa")
        self.passwords = dict()

        # 实例化数据加载对象
        self.loader = DataLoader()

        # 实例化我们的ResultCallback，用来处理结果。
        self.results_callback = ResultCallback()

        # 实例化解析结果的对象
        self.get_result = GetResult(self.results_callback)

        self.inventory, self.variable_manager = self.load_inventory_variable()

        self.play_hosts_list = []

    def load_inventory_variable(self):
        # create inventory and pass to var manager
        # 创建 资源库对象，并传递给 变量管理器
        inventory = InventoryManager(
            loader=self.loader,  # 用于加载和处理 json、yaml 文件的数据管理器
            sources=["%s/conf/hostlist" % BASE_DIR] # 是一个或者多个文件。 相当于 /etc/ansible/inventory.py
            )
        variable_manager = VariableManager(loader=self.loader, inventory=inventory)

        """
            add hosts to a group
        """
        # 向资源池对象里添加一个组
        group_name = 'group1'
        inventory.add_group(group_name)

        hosts_list = [{"hostname": 'gjzfapp1', 'manage_ip': '172.16.153.130', 'port': 22, 'remote_user': 'shark', 'password': 'upsa/upsa', "key": '/Users/yanshunjun/.ssh/id_rsa'},
                      {"hostname": 'gjzfapp2', 'manage_ip': '172.16.153.131', 'port': 22, 'remote_user': 'root', 'password': 'upsa', "key": '/Users/yanshunjun/.ssh/id_rsa'},]
        # 添加主机到上面我们创建的组
        for host in hosts_list:
            # 设置远程连接信息
            host_name = host.get("hostname")
            host_ip = host.get("manage_ip", host_name)
            host_port = host.get("port", 22)
            remote_user = host.get("remote_user")
            password = host.get("password")
            key = host.get("key")
            # {"gjzfap1.com": {"hostname": "gjzfap1.com", "manage_ip": "172.16.153.130", "port": 22,
            #                  "auth_type": 0, "remote_user": "shark", "password": "upsa/upsa"}}

            # 创建这个主机对象
            host_obj = Host(name=host_ip)

            # 把 SSH 连接信息赋值给这个主机对象的变量
            variable_manager.set_host_variable(host=host_obj, varname="ansible_ssh_host", value=host_ip)
            variable_manager.set_host_variable(host=host_obj, varname="ansible_ssh_pass", value=password)
            variable_manager.set_host_variable(host=host_obj, varname="ansible_ssh_port", value=host_port)
            variable_manager.set_host_variable(host=host_obj, varname="ansible_ssh_user", value=remote_user)
            # self.variable_manager.set_host_variable(host=my_host, varname='ansible_ssh_private_key_file', value=ssh_key)
            variable_manager.set_host_variable(host=host_obj, varname='ansible_ssh_private_key_file', value=key)

            # 最后把这个主机添加到组里

            inventory.add_host(host=host_ip, group=group_name)
            new_host_obj = inventory.get_host(host_ip)
            print(variable_manager.get_vars(host=new_host_obj))
        return inventory, variable_manager

    # def dynamic_inventory(self, task_resource):
    #     """
    #         add hosts to inventory.
    #     """
    #     self.task_resource = task_resource
    #
    #     if isinstance(self.task_resource, list):
    #         self.add_dynamic_group(hosts_list=self.task_resource, group_name="task_group")
    #     elif isinstance(self.task_resource, dict):
    #         for group_name, hosts_item in self.task_resource.items():
    #             self.add_dynamic_group(hosts_item.get("manage_ip"), group_name, hosts_item.get("vars"))

    def adhoc_runner(self):
        self.play_hosts_list = ['172.16.153.130', '172.16.153.131']
        # create play with tasks
        # 创建任务
        play_source = dict(
            name="Ansible adhoc Play",  # 名字是自定义的
            hosts=self.play_hosts_list,
            gather_facts="no",
            tasks=[
                dict(action=dict(module='shell', args='whoami'), register="user"),
                dict(action=dict(module="debug", args=dict(msg="{{user}}")))
            ]
        )

        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        # actually run it
        # 实际运行它
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,                # 资源池对象
                variable_manager=self.variable_manager,  # 管理目标的变量
                loader=self.loader,                      # 加载并处理需要用到的变量等数据
                options=self.options,                    # 执行任务时，需要用到哪些选项
                passwords={},                # 执行任务时用到的全局密码，可以为一个空字典{}
                stdout_callback=self.results_callback)        # 使用我们的自定义回调代替“default”回调插件

            constants.HOST_KEY_CHECKING = True          # 不检查对方公钥

            status_code =tqm.run(play)
            print('status_code', status_code)

            """
            """
        except Exception as e:
            print(traceback.print_exc())
        finally:
            if tqm is not None:
                tqm.cleanup()


class GetResult(object):
    def __init__(self, res_callback):
        self.results_dic = {"success": {}, "failed": {}, "unreachable": {}}
        self.res_callback = res_callback

    def get_model_result(self):
        for host, result_obj in self.res_callback.host_ok.items():
            host = host.replace(".", ":")
            self.results_dic["success"][host] = result_obj._result

        for host, result_obj in self.res_callback.host_failed.items():
            host = host.replace(".", ":")
            self.results_dic["failed"][host] = result_obj._result

        for host, result_dict in self.res_callback.host_unreachable.items():
            host = host.replace(".", ":")
            self.results_dic["unreachable"][host] = result_dict['msg']

        return self.results_dic

    def get_playbook_result(self):
        self.results_dic = {"skipped": {}, "failed": {}, "ok": {}, "status": {}, "unreachable": {}, "changed": {}}
        for host, result_obj in self.res_callback.task_ok.items():
            host = host.replace(".", ":")
            self.results_dic["ok"][host] = result_obj

        for host, result_obj in self.res_callback.task_failed.items():
            host = host.replace(".", ":")
            self.results_dic["failed"][host] = result_obj

        for host, result_obj in self.res_callback.task_status.items():
            host = host.replace(".", ":")
            self.results_dic["status"][host] = result_obj

        for host, result_obj in self.res_callback.task_skipped.items():
            host = host.replace(".", ":")
            self.results_dic["skipped"][host] = result_obj

        for host, result_obj in self.res_callback.task_unreachable.items():
            host = host.replace(".", ":")
            self.results_dic["unreachable"][host] = result_obj['msg']
        return self.results_dic

if __name__ == "__main__":
    ansi = Run()
    ansi.adhoc_runner()
    res = ansi.get_result.get_model_result()
    print('res', res)
