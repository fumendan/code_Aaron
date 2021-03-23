import json
from django.shortcuts import render, HttpResponse
from django.views.generic import View, ListView, DateDetailView
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from utils.pagination import Pagination
from db import models
# Create your views here.


def base(request):
    return render(request, 'base.html')


class IndexView(View):
    def get(self,request):
        return render(request, 'cmdb/dash_board.html')


def dash_board(request):
    data_dict = {'asset_status': None, 'asset_type': None}
    status_qs = list(models.Asset.objects.values_list('device_status_id').annotate(value=Count('device_status_id')))
    type_qs = list(models.Asset.objects.values_list('device_type_id').annotate(value=Count('device_type_id')))
    status_lists = [list(item) for item in status_qs]
    type_lists = [list(item) for item in type_qs]

    for i, item in enumerate(status_lists):
        for k, v in models.Asset.device_status_choices:
            if item[0] == k:
                status_lists[i][0] = v

    for i, item in enumerate(type_lists):
        for k, v in models.Asset.device_type_choices:
            if item[0] == k:
                type_lists[i][0] = v

    data_dict['asset_status'] = status_lists
    data_dict['asset_type'] = type_lists
    print('-->',data_dict)
    return HttpResponse(json.dumps(data_dict))


class AssetListView(View):
    """
    使用方式：
    all_count = models.UserInfo.objects.all().count()
    page_info = PageInfo(request.GET.get('p'),10,all_count,request.path_info)
    user_list = models.UserInfo.objects.all()[page_info.start():page_info.end()]

    :param current_page:  当前页
    :param per_page_num:  每页显示数据条数
    :param all_count:  数据库总个数
    :param base_url:  页码标签的前缀
    :param page_range:  页面最多显示的页码个数
    """

    """
    models.MyModel.objects.all()
    优化： 对于包含有 Fk 字段的表，当需要取出对应表里的某一条数据的一个字段的话，
    Django 会在每次循环一条数据的时候，就用外键的 ID 到对应的表里查询这个 ID 
    对应要展示的字段名。所以 IDC 表中有几条数据，就会到对应的表里查询多少次。
    
    优化办法：
    models.MyModel.objects.all().select_related('FK_field')
    这样就会在第一次查询时，把 Fk 的字段对应表的数据全部查询到。
    
    用 values、values_list 是不存在上述情况的
    models.MyModel.objects.values('user_name')
    """


    def get(self, request):
        choices_dict = {'status': {}, 'type': {}}
        dev_status_dict = dict(models.Asset.device_status_choices)
        dev_type_dict = dict(models.Asset.device_type_choices)

        dev_status_dict[0] = '------'
        dev_type_dict[0] = '------'

        p = request.GET.get('p')
        base_url = request.path_info

        try:
            page_by = int(request.GET.get('page_by', 5))
        except ValueError:
            page_by = 5

        # 三元运算
        search_status = int(request.GET.get('search_status', )) if request.GET.get('search_status') else 0
        search_type = int(request.GET.get('search_type')) if request.GET.get('search_type') else 0

        if all([search_status, search_type]):
            choices_dict['status'][search_status] = dev_status_dict[search_status]
            choices_dict['type'][search_type] = dev_type_dict[search_type]

            queryset = models.Asset.objects.filter(device_status_id=search_status, device_type_id=search_type)
            all_count = queryset.count()
        elif any([search_status, search_type]):
            choices_dict['status'][search_status] = dev_status_dict[search_status]
            choices_dict['type'][search_type] = dev_type_dict[search_type]

            queryset = models.Asset.objects.filter(Q(device_status_id=search_status) | Q(device_type_id=search_type))
            all_count = queryset.count()
        else:
            choices_dict['status'][search_status] = dev_status_dict[search_status]
            choices_dict['type'][search_type] = dev_type_dict[search_type]
            queryset = models.Asset.objects.all()
            all_count = queryset.count()
        base_url = "{}?search_status={}&search_type={}".format(base_url, search_status, search_type)
        page_obj = Pagination(p, page_by, all_count, base_url)
        page_obj.page_by = page_by

        asset_list = queryset[page_obj.start():page_obj.end()]

        return render(request, 'cmdb/asset_list.html', {'asset_list': asset_list,
                                                        'page_obj': page_obj,
                                                        'choices_dict': choices_dict,
                                                        'dev_status_dict': dev_status_dict,
                                                        'dev_type_dict': dev_type_dict,
                                                        })


class IdcView(ListView):

    queryset = models.IDC.objects.all()
    context_object_name = 'idc_obj'
    template_name = 'cmdb/idc.html'


class HostDetailView(View):
    def get(self, request, asset_id):
        """
        asset hostname  manage_ip machine
        sn manufacturer model

        os_name os_version kernel model_name
        cpu_type physical_count physical_cores  processor_cores_count
        latest_date create_at
        """
        asset_queryset = models.Asset.objects.filter(id=asset_id)

        if asset_queryset.exists():
            asset_obj = asset_queryset.get()

            memory_fields = ('slot', 'capacity', 'model', 'speed', 'manufacturer')
            disk_fields = ('slot', 'capacity', 'pd_type', 'model')
            nic_fields = ('name', 'ipaddrs', 'netmask', 'hwaddr')
            asset_change_log_fields = ('create_at', 'content', 'operator__email')

            server_dict = models.Server.objects.filter(asset=asset_id).values().first()

            server_id = server_dict['id']

            memory_queryset = models.Memory.objects.filter(server_obj=server_id).values_list(*memory_fields)
            disk_queryset = models.Disk.objects.filter(server_obj=server_id).values_list(*disk_fields)
            nic_queryset = models.NIC.objects.filter(server_obj=server_id).values_list(*nic_fields)

            change_log_qs = models.AssetChangLog.objects.filter(server_obj=server_id).all().values(*asset_change_log_fields)

            for item in change_log_qs:
                item['content'] = eval(item['content'])

            return render(request, 'cmdb/host_detail.html', {'asset_obj': asset_obj,
                                                             'server_dict': server_dict,
                                                             'memory': memory_queryset,
                                                             'disk': disk_queryset,
                                                             'nic': nic_queryset,
                                                             'asset_id': asset_id,
                                                             'change_log_dict': change_log_qs,
                                                             })
        else:
            return render(request, 'pages-error-404.html')


class BusinessView(ListView):
    queryset = models.AppClass.objects.all()
    context_object_name = 'business_obj'
    template_name = 'cmdb/business.html'


class DepartmentList(ListView):
    queryset = models.Department.objects.all()
    context_object_name = 'department_obj'
    template_name = 'cmdb/department.html'


def get_change(request):
    """
    获取变更信息
    :param request:
    :return:
    """
    change_obj = models.AssetChangLog.objects.filter(server_obj=4).all()
    change_info = []
    for item in change_obj:
        change_info.extend(item.content.split('|'))
    print(change_info)
    return render(request, 'cmdb/change_info.html', {'change_info': change_info})

