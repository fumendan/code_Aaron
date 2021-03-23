import json
import traceback
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.transaction import atomic
from .utils import api_auth
from db import models


@csrf_exempt
@api_auth
def asset(request):
    asset_str = request.body.decode()
    asset_dict = json.loads(asset_str)
    if not asset_dict['base_info']['status']:
        return HttpResponse("获取资产信息的状态不纯洁，数据不通过")
    report_host_dict = asset_dict['base_info']['data']
    host_name = report_host_dict['hostname']

    server_obj = models.Server.objects.filter(hostname=host_name).first()

    if not server_obj:
        # 创建服务器信息(基本信息、主板、CPU)、网卡、内存、硬盘等信息
        server_info = {}
        server_info.update(asset_dict['base_info']['data'])
        server_info.update(asset_dict['motherboard']['data'])
        server_info.update(asset_dict['cpu']['data'])
        try:
            # 服务器信息
            with atomic():
                server_obj = models.Server.objects.create(**server_info)

                # 内存
                memory_info = asset_dict['memory']['data']
                for memory_item in memory_info.values():
                    memory_item['server_obj'] = server_obj
                    models.Memory.objects.create(**memory_item)

                # 硬盘
                disk_info = asset_dict['disk']['data']
                for disk_item in disk_info.values():
                    disk_item['server_obj'] = server_obj
                    models.Disk.objects.create(**disk_item)

                # 网卡
                nic_info = asset_dict['nic']['data']
                for nic_name, nic_item in nic_info.items():
                    nic_item['server_obj'] = server_obj
                    nic_item['name'] = nic_name
                    models.NIC.objects.create(**nic_item)
            asset_report_template = " [ 资产首次上报 ]  资产主机名 {} ， 资产类型 Server"
            asset_report_list = []

            asset_report_info = asset_report_template.format(host_name)

            asset_report_list.append(asset_report_info)
            if asset_report_list:
                models.AssetChangLog.objects.create(server_obj=server_obj, content=asset_report_list)

        except Exception as e:
            print(traceback.format_exc())
            return HttpResponse('数据存库失败，{}'.format(traceback.format_exc()))

        return HttpResponse("The reported asset information was created successfully")

    else:
        # 数据库中已经存在此资产信息，需要对比新旧资产信息，并进行相应的更新

        # 服务器表
        new_server_info = {}
        new_server_info.update(asset_dict['base_info']['data'])
        new_server_info.update(asset_dict['motherboard']['data'])
        new_server_info.update(asset_dict['cpu']['data'])

        log_template = "资产 [ {} ] 的 [ {} ] 由 [ {} ] 变更为： [ {} ]"
        log_info_list = []
        try:
            with atomic():
                for k, new_val in new_server_info.items():

                    # 通过反射，得到数据库中的值
                    old_val = getattr(server_obj, k)

                    if old_val != new_val:
                        setattr(server_obj, k, new_val)
                        log_info = log_template.format(host_name, k, old_val, new_val)
                        log_info_list.append(log_info)
                server_obj.save()

                if log_info_list:
                    models.AssetChangLog.objects.create(server_obj=server_obj, content=log_info_list)
        except Exception:
            print(traceback.format_exc())
            return HttpResponse("资产{}的{}数据更新失败".format(host_name, 'base_info'))

        ################
        #     内存表
        ################
        new_memory_dict = asset_dict['memory']['data']
        new_memory_slot_set = set(new_memory_dict)
        old_memory_slot_set = {i.slot for i in server_obj.memory.all()}

        add_slot_set = new_memory_slot_set - old_memory_slot_set  # new_set.difference(old_set)
        del_slot_set = old_memory_slot_set - new_memory_slot_set  # old_set.difference(new_set)

        memory_obj = models.Memory.objects

        # 增加内存数据
        add_mem_log_info_list = []
        add_log_template = "资产 [ {} ] 的 {} 数据增加 了 [ {} ]"
        try:
            for slot in add_slot_set:
                add_memory_info = new_memory_dict[slot]
                add_memory_info['server_obj'] = server_obj

                with atomic():
                    memory_obj.create(**add_memory_info)
                    add_memory_info['server_obj'] = server_obj.hostname
                    add_mem_log_info = add_log_template.format(host_name, '内存', add_memory_info)
                    add_mem_log_info_list.append(add_mem_log_info)

            if add_mem_log_info_list:
                models.AssetChangLog.objects.create(server_obj=server_obj, content=add_mem_log_info_list)
        except Exception:
            print(traceback.format_exc())

        # 删除内存数据
        del_mem_log_list = []
        del_mem_log_template = "资产 [ {} ] 的 {} 数据删除了 [ {} ]"
        try:
            with atomic():
                del_memory_obj = memory_obj.filter(server_obj=server_obj, slot__in=del_slot_set)

                # 获取到表的所有字段名
                fields_list = [i.column for i in models.Memory._meta.fields]

                # 获取到需要删除的每条记录详细信息，用于做记录用
                del_memory_dict = list(del_memory_obj.values(*fields_list))
                # 删库跑路
                if del_memory_obj:
                    del_memory_obj.delete()

                    # 跑不了，这里有记录呢！！！
                    for item in del_memory_dict:
                        item['server_obj'] = server_obj.hostname
                        del_log_info = del_mem_log_template.format(host_name, '内存', item)
                        del_mem_log_list.append(del_log_info)

                    # 记录操作日志，保存好证据
                    if del_mem_log_list:
                        models.AssetChangLog.objects.create(server_obj=server_obj, content=del_mem_log_list)

        except Exception:
            print(traceback.format_exc())

        # 更新内存表
        # 汇报的新资产信息中有的，数据库中也有的，需要对比每条记录的每个字段，并进行更新
        update_slot_set = new_memory_slot_set & old_memory_slot_set  # new_set.intersection(old_set)

        up_mem_log_template = "资产 [ {} ] 的 {} 数据有变更，其中 [ {} ] 槽位的 [ {} ] 由 [ {} ] 变更为 [ {} ]"

        for slot in update_slot_set:
            up_mem_log_list = []
            # 获取到需要更新的数据中的每一条记录
            up_mem_info = new_memory_dict[slot]
            up_memory_obj = memory_obj.filter(server_obj=server_obj, slot=slot).first()

            # 对于获取到的这一条数据和对应的数据库中的数据进行逐个字段的对比，并进行更新
            for k, new_val in up_mem_info.items():
                old_val = getattr(up_memory_obj, k)
                print(new_val, '___>', old_val)
                if new_val != old_val:
                    setattr(up_memory_obj, k, new_val)
                    if k == 'server_obj':
                        print('yan', new_val)
                    up_mem_log_info = up_mem_log_template.format(host_name, '内存', slot, k, old_val, new_val)
                    up_mem_log_list.append(up_mem_log_info)
            up_memory_obj.save()

        if up_mem_log_list:
            print('up_mem_log_list', up_mem_log_list)
            models.AssetChangLog.objects.create(server_obj=server_obj, content=up_mem_log_list)

        ################
        #     硬盘表
        ################

        return HttpResponse('资产已更新')
