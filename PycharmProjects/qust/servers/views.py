from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from db import models
import json


# Create your views here.
class DashboardView(View):
    def get(self, request):
        return render(request, 'dashboard.html')


class IDCManager(View):
    def get(self, request):
        idc_obj = models.ServerMachine.objects.all().values()
        return render(request, 'idc_manager.html', {'idc_obj': idc_obj})


class ServerManager(View):
    def get(self, request):
        return render(request, 'server_manager.html')


def dash_board(request):
    data_dict = {'asset_status': ['上线', '离线'], 'asset_type': [8, 5]}
    return HttpResponse(json.dumps(data_dict))


def add_server(request):
    if request.method == 'POST':
        server_ip = request.POST.get('server_ip')
        hostname = request.POST.get('hostname')
        os = request.POST.get('os')
        cpu_kernel = request.POST.get('cpu_kernel')
        mem_total = request.POST.get('mem_total')
        mem_used = request.POST.get('mem_used')
        disk_capacity = request.POST.get('disk_capacity')
        if server_ip is not None and hostname is not None and os is not None and cpu_kernel is not None \
                and mem_total is not None and mem_used is not None and disk_capacity is not None:
            ser = {'server_ip': server_ip, 'hostname': hostname,
                   'os': os, 'cpu_kernel': cpu_kernel,
                   'mem_total': mem_total,
                   'mem_used': mem_used, 'disk_capacity': disk_capacity}
            models.ServerMachine.objects.create(**ser)
            return HttpResponse('保存成功！')
        else:
            return HttpResponse('保存失败！')
    else:
        print('---->')
        return render(request, 'server_manager.html')
