
import os
import json
import traceback
import time
from datetime import datetime

# 把一个 Queryset 对象转换为字典
from django.forms.models import model_to_dict
from django.shortcuts import render, HttpResponse
from SharkAPAMP.settings import MODULES_DIRS
from django.views.generic import View, ListView
from .forms.oct_form import OctopusForm, TaskForm
from db.models import ModuleInfo, InventoryHosts
from octopus.utils.task_hosts_handler import TaskDataHandler
from octopus.utils.ansiblev2api import Run
from db.mongohandler import Mongodb
from bson.objectid import ObjectId
from utils.cipher import Crypto
from SharkAPAMP import settings
from db import models


def canvas(request):
    return render(request, 'octopus/canvas_timeline.html')


class BaseResponse:
    def __init__(self):
        self.status = False
        self.data = ''
        self.error = ''


class InventoryView(ListView):
    queryset = InventoryHosts.objects.all()
    context_object_name = 'inventory_list_obj'
    template_name = 'octopus/inventory.html'


class ModuleView(View):
    def get(self, request):
        """
        GET 请求的来的，假如是编辑，就先到数据库中取出对象对应的字段的值,
        成功取到后，初始化 Form 表单，之后展示到前端。
        假如没有取出，就把数据库中的所有对象取出来，并跳转到展示网页。

        :param request:
        :return:
        """

        try:
            module_id = int(request.GET.get('module_id'))

            module_fields = ['module_name', 'module_type', 'module_lang',
                             'module_info', 'module_path']
            module_dict = ModuleInfo.objects.filter(id=module_id).values(*module_fields).first()

            form_obj = OctopusForm(initial=module_dict)
            return render(request, 'octopus/edit_models.html', {'form_obj': form_obj})
        except Exception as e:
            # 说明给的模块 id 不对，或者有其他异常, 返回到模块详情预览页面
            print('except', e)
            module_obj = ModuleInfo.objects.all()

            return render(request, 'octopus/models_detail.html', {"module_obj": module_obj})

    def post(self, request):
        module_map = {"1": "ansible", "2": "shell", "3": "salt"}

        res = BaseResponse()
        form_obj = OctopusForm(request.POST, request.FILES, auto_id='id_%s')
        if form_obj.is_valid():
            # 获取标识
            module_tag = request.POST.get('module_type', '')
            map_str = module_map[module_tag]

            # 获取到存放目录
            modules_dir = MODULES_DIRS[map_str]

            if not os.path.exists(modules_dir):
                os.makedirs(modules_dir)
            file_obj = form_obj.cleaned_data.get('module_file')

            file_full_path = "{}{}".format(modules_dir, file_obj.name)

            try:
                with open(file_full_path, 'wb+') as f:
                    for chunk in file_obj.chunks():  # 分块写入文件
                        f.write(chunk)

                # 添加模块路径
                form_obj.cleaned_data['module_path'] = file_full_path

                # 从清理后的数据里，删除文件对象
                form_obj.cleaned_data.pop('module_file')

                ModuleInfo.objects.update_or_create(**form_obj.cleaned_data)

                res.status = True
                res.data = '模块上传成功'

            except Exception as e:
                res.error['save_status'] = {"message": "上传失败-{}".format(e)}

        else:
        #     pass
        # return render(request, 'octopus/models_1.html', {"form_obj": form_obj})

            error_msg = form_obj.errors.as_json()
            res.error = json.loads(error_msg)
        return HttpResponse(json.dumps(res.__dict__))


class AddModuleView(ModuleView):
    def get(self, request):
        form_obj = OctopusForm()

        return render(request, 'octopus/edit_models.html', {"form_obj": form_obj})


class TaskView(View):
    def get(self, request):
        task_form_obj = TaskForm()
        from octopus.utils.get_inventory_hosts import GetInventoryHosts
        get_invent_h_g =GetInventoryHosts()

        inventory_hosts = get_invent_h_g.mathode2()
        """
        inventory_hosts = {'gjzf': [{'host_ip': '172.16.153.130', 'host_name': 'gjzfap1.com'}, 
                                    {'host_ip': '172.16.153.131', 'host_name': 'gjzfap2.com'}], 
                           'qudao': [{'host_ip': '172.16.153.132', 'host_name': 'argap1.com'}, 
                                    {'host_ip': '172.16.153.133', 'host_name': 'argap2.com'}],
                           'gjzf_child1': [{'host_ip': '172.16.153.134', 'host_name': 'amonap1.com'}], 
                           'gjzf_chid2': [{'host_ip': '172.16.153.135', 'host_name': 'yargap1.com'}], 
                           'gjzf_child1_1': [{'host_ip': '8.8.8.8', 'host_name': 'bargap4.com'}], 
                           'un_group': [{'host_ip': '1.1.1.1', 'host_name': 'bargap3.com'}, 
                                        {'host_ip': '9.9.9.9', 'host_name': 'bmonap1.com'}]}

        """

        return render(request, 'octopus/tasks.html', {'task_form_obj': task_form_obj,
                                                      "inventory_hosts": inventory_hosts})

    def post(self, request):
        invent_hosts_id = request.POST.get('select_hosts_id')
        invent_hosts_id = json.loads(invent_hosts_id)
        task_form_obj = TaskForm(request.POST)
        """
           record_format = {"process_info": [
                                             {"status_code": "1001", "update_time": datetime.datetime.now()}
                                            ],
                            "start_time": self.start_time,
                            "task_content": "{...}"
                            }
        """
        mongo_handler1 = Mongodb()
        start_time = time.strftime("%Y-%m-%d %X")

        # 记录任务事件到 mongo
        record_content = {
                          "process_info": [
                                          {"status_code": "1000",
                                           "detail": settings.TASK_STATUS_CODE["1000"],
                                           "update_time": str(datetime.now())},
                                       ],
                          "start_time": start_time,
                         }

        task_id_obj = mongo_handler1.insert(record_content)

        if task_form_obj.is_valid():
            task_form_obj.cleaned_data["invent_hosts_id"] = invent_hosts_id

            """
            {'module_name': 7, 'remote_user': 1, 'module_type': 1, 
            'exec_args': 'ls /tmp', 'invent_hosts_id': ['6', '7']}
            """

            """
            def push(self, id_obj, array_key, array_value):
                return self.col.update({"_id": id_obj}, {"$push": {array_key: array_value}})
            """

            mongo_handler1.push(task_id_obj,
                                "process_info", {"status_code": "1001",
                                                 "detail": settings.TASK_STATUS_CODE["1001"],
                                                 "update_time": str(datetime.now())
                                                 }
                                )

            try:
                pid = os.fork()
                # 关闭父进程的 MongoClient 实例
                mongo_handler1.client.close()
                if pid == 0:
                    # PyMongo不是安全的。使用 MongoClient 的实例时必须小心 fork()。
                    # 具体来说，MongoClient的实例不能从父进程复制到子进程。
                    # 相反，父进程和每个子进程必须创建他们自己的MongoClient实例。
                    # 由于 fork() 内的描述的线程和锁之间固有的不兼容性，从父进程复制的MongoClient实例在子进程中很有可能发生死锁。如果发生这种死锁，PyMongo会尝试发出警告
                    # 官方文档： http://api.mongodb.com/python/current/faq.html#is-pymongo-fork-safe
                    mongo_handler2 = Mongodb()

                    mongo_handler2.push(task_id_obj,
                                        "process_info", {"status_code": "1002",
                                                         "detail": settings.TASK_STATUS_CODE["1002"],
                                                         "update_time": str(datetime.now())
                                                         }
                                        )

                    task_data_handler = TaskDataHandler(task_form_obj.cleaned_data)

                    task_resource, module_name = task_data_handler.get_data()
                    print('yan-->', task_resource,module_name)

                    """
                    [{'remote_user': 'shark', 'password': 'upsa/upsa', 'port': 22, 'manage_ip': '172.16.153.130', 'host_name': 'gjzfap1.com'}, 
                     {'remote_user': 'shark', 'password': 'upsa/upsa', 'port': 22, 'manage_ip': '172.16.153.131', 'host_name': 'gjzfap2.com'}, 
                     {'select_hosts_list': ['172.16.153.130', '172.16.153.131']}] 
                    
                    shell
                    """

                    ansible_handler = Run()

                    mongo_handler2.push(task_id_obj,
                                        "process_info", {"status_code": "1003",
                                                         "detail": settings.TASK_STATUS_CODE["1003"],
                                                         "update_time": str(datetime.now())
                                                         }
                                        )

                    ansible_handler.adhoc_runner(task_id_obj=task_id_obj,
                                                 recorder=mongo_handler2,
                                                 task_resource=task_resource,
                                                 module_name=module_name,
                                                 args=task_form_obj.cleaned_data['exec_args'])

                    mongo_handler2.push(task_id_obj,
                                        "process_info", {"status_code": "2000",
                                                         "detail": settings.TASK_STATUS_CODE["2000"],
                                                         "update_time": str(datetime.now())
                                                         }
                                        )

                    # 获取任务执行结果
                    info = ansible_handler.get_result.get_model_result()

                    mongo_handler2.col.update({"_id": task_id_obj},
                                              {"$push": {"process_info": {"status_code": "2001",
                                                                          "detail": settings.TASK_STATUS_CODE["2001"],
                                                                          "update_time": str(datetime.now())
                                                                          },
                                                         },
                                               "$set": {"task_content": info}
                                               },
                                              )
                    mongo_handler2.push(task_id_obj,
                                        "process_info", {"status_code": "2002",
                                                         "detail": settings.TASK_STATUS_CODE["2002"],
                                                         "update_time": str(datetime.now())
                                                         }
                                        )
                    mongo_handler2.client.close()
                else:
                    return HttpResponse(json.dumps({"task_id": str(task_id_obj)}))
            except OSError as oser:
                mongo_handler1.push(task_id_obj,
                                    "process_info", {"status_code": "5001",
                                                     "detail": settings.TASK_STATUS_CODE["5001"],
                                                     "update_time": str(datetime.now())
                                                     }
                                    )
                return HttpResponse(json.dumps({"task_id": str(task_id_obj)}))
        return HttpResponse(json.dumps({"info": "参数有误"}))


class GetTaskInfoView(View):
    def get(self, request):
        task_id_str = request.GET.get("task_id")
        task_id_obj = ObjectId(task_id_str)
        status_code = settings.TASK_STATUS_CODE
        mongo = Mongodb()

        result = mongo.filter_one({"_id": task_id_obj},  # 查询条件
                                  {"process_info": 1, "start_time": 1,
                                   "task_content": True, "_id": False}  # 过滤的字段
                                  )
        if isinstance(result, dict):
            return HttpResponse(json.dumps(result))
        else:
            result = {"process_info": {"status_code": "4000",
                                       "detail": settings.TASK_STATUS_CODE["4000"],
                                       "update_time": ""
                                       },
                      "start_time": "查询时间{}".format(str(datetime.now()))
                      }
            return HttpResponse(json.dumps(result))

    def post(self, request):
        print(request.POST)
        return HttpResponse("你来啦")
        """
           resource = {}
                    hosts_list = []
                    vars_dic = {}
                    cn = prpcrypt()
                    hosts_ip = []
                    for host in hosts_obj:
                        sshpasswd = cn.decrypt(host.ssh_userpasswd)
                        if host.ssh_type in (1,2):
                            resource =  {
                                "dynamic_host": {
                                    "hosts": [
                                                {"hostname": "192.168.1.108", "port": "22", "username": "root", "ssh_key": "/etc/ansible/ssh_keys/id_rsa"},
                                                {"hostname": "192.168.1.109", "port": "22", "username": "root","ssh_key": "/etc/ansible/ssh_keys/id_rsa"}
                                              ],
                                    "vars": {
                                             "var1":"ansible",
                                             "var2":"saltstack"
                                             }
                                }
                            }
                            hosts_list.append({"hostname":host.sn_key,"ip":host.ssh_hostip,"port":host.ssh_host_port,"username":host.ssh_username,"ssh_key":host.ssh_rsa})
                            hosts_ip.append(host.sn_key)
        """





        """
        resource['test_g']={"hosts": [{"hosname": 'shark', "ip": '172.16.151.1310', "port": 22,"username": "shark","ssh_key": "", "password": "upsa"},]}
        """
