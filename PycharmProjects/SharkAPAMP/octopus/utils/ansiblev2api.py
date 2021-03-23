#!/usr/bin/env python
# -*- coding:utf-8 -*-

import traceback
from datetime import datetime
from collections import namedtuple

# 第三方
from ansible import constants
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.inventory.host import Host, Group

# 自定义
from SharkAPAMP.settings import BASE_DIR, TASK_STATUS_CODE
from .parse_data import DynamicInventory



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


class Run(MyOptions, DynamicInventory):
    def __init__(self, *args, **kwargs):
        """
        多重集成，需要显式调用父类的构造方法
        :param args:
        :param kwargs:
        """
        MyOptions.__init__(self, *args, **kwargs)
        DynamicInventory.__init__(self, *args, **kwargs)

        # 设置一个密码对象，字典类型, key 可以自定义, 这个是必须参数，但是可以为空
        # passwords = dict(vault_pass="upsa/upsa")
        self.passwords = dict()

        # 实例化我们的ResultCallback，用来处理结果。
        self.adhoc_callback = ResultCallback()
        self.play_callback = PlayBookResultsCollector()

        # 实例化解析结果的对象, 用于格式化输出结果
        self.get_result = GetResult(self.adhoc_callback)
        self.get_playbook_result = GetResult(self.play_callback)

    def add_host_connection_info(self, task_resource_list):
        """
            add hosts to a group
        """
        """
        [
         {'remote_user': 'shark', 'password': 'upsa/upsa', 'port': 22, 'manage_ip': '172.16.153.130', 'host_name': 'gjzfap1.com'}, 
         {'remote_user': 'shark', 'password': 'upsa/upsa', 'port': 22, 'manage_ip': '172.16.153.131', 'host_name': 'gjzfap2.com'}, 
         {'select_hosts_list': ['172.16.153.130', '172.16.153.131']}
        ] 
        """
        inventory_hosts_dict = self.inventory.hosts

        for item in task_resource_list:
            if 'select_hosts_list' in item.keys():
                select_hosts_list = item.pop('select_hosts_list')
                self.play_hosts_list = select_hosts_list
                for s_host in select_hosts_list:
                    # 先判断选择的主机是否已经在资源库中
                    if s_host not in inventory_hosts_dict.keys():
                        # 选择的主机不在资源仓库里
                        print("选择的主机不在资源仓库里, 准备动态添加")

                        # 调用父类 DynamicInventory 的实例方法，添加主机到默认组
                        self.add_host_to_group(s_host, 'default_group')

        for item in task_resource_list:
            # 获取连接信息
            host_name = item.get("host_name")
            host_ip = item.get("manage_ip", host_name)
            host_port = item.get("port", 22)
            remote_user = item.get("remote_user")

            # 创建这个主机对象
            host_obj = Host(name=host_ip, port=host_port)

            # 为这个主机对象设置 SSH 连接信息
            self.variable_manager.set_host_variable(host=host_obj, varname="ansible_ssh_host", value=host_ip)
            self.variable_manager.set_host_variable(host=host_obj, varname="ansible_ssh_port", value=host_port)
            self.variable_manager.set_host_variable(host=host_obj, varname="ansible_ssh_user", value=remote_user)
            self.variable_manager.set_host_variable(host=host_obj, varname="ansible_ssh_private_key_file", value='/Users/yanshunjun/.ssh/id_rsa')

    def adhoc_runner(self, task_resource, module_name, args, task_id_obj=None, recorder=None):
        # 先调用实例方法，把每个主机的 SSH 连接信息，添加到资源库的变量里；并返回目标主机 ip 列表
        self.add_host_connection_info(task_resource)
        # 创建任务
        play_source = dict(
            name="Ansible Play",  # 名字是自定义的
            hosts=self.play_hosts_list,
            gather_facts="no",
            tasks=[
                dict(action=dict(module=module_name, args=args), register="shell_out"),
                dict(action=dict(module="debug", args=dict(msg="{{shell_out}}")))
            ]
        )

        # 向 Mongodb 记录任务执行过程的状态
        recorder.push(task_id_obj,
                      "process_info", {"status_code": "1004",
                                       "detail": TASK_STATUS_CODE["1004"],
                                       "update_time": str(datetime.now())
                                       }
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
                stdout_callback=self.adhoc_callback)        # 使用我们的自定义回调代替“default”回调插件

            constants.HOST_KEY_CHECKING = False          # 不检查对方公钥

            tqm.run(play)

            """
            """
        except Exception as e:
            print(traceback.print_exc())
        finally:
            if tqm is not None:
                tqm.cleanup()

    def run_playbook(self, playbook_path, extra_vars=None):
        """
        run ansible palybook
        """
        try:
            if extra_vars: self.variable_manager.extra_vars = extra_vars
            executor = PlaybookExecutor(
                playbooks=[playbook_path],
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
            )
            executor._tqm._stdout_callback = self.play_callback
            constants.HOST_KEY_CHECKING = False
            executor.run()
        except Exception:
            return False


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
            self.results_dic["unreachable"][host] = result_obj
        return self.results_dic



