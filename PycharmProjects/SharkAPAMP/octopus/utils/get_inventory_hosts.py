#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 调试此模块时，打开下面的注释
import os, sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath('__file__'))))
# print(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)
os.environ["DJANGO_SETTINGS_MODULE"] = 'SharkAPAMP.settings'
import django
django.setup()
# 设置 Django 环境结束
try:
    from db import models
    from django.db.models import F
except Exception as e:
    import sys
    print('打开此文件，最上面几行的注释，设置 Django 的环境')
    sys.exit(e)


class GetInventoryHosts(object):
    """
    返回的数据：
    {'gjzf': ['172.16.153.130', '172.16.153.131'], 'qudao': ['172.16.153.132', '172.16.153.133'],
    'gjzf_child1': ['172.16.153.134'], 'gjzf_chid2': ['172.16.153.135'], 'gjzf_child1_1': ['8.8.8.8'],
    'un_group': ['1.1.1.1', '9.9.9.9']}
    """
    def __init__(self):
        pass

    def mathode2(self):
        _dic2 = {}
        for ig in models.InventoryGroups.objects.all():
            host_item_li = [host_obj for host_obj in ig.inventoryhosts_set.annotate(host_name=F('host__hostname')
                                                                                    ).values('id', 'host_name')]
            if host_item_li:
                _dic2[ig.group_name] = host_item_li
                # [{'host_ip': '172.16.153.130', 'host_name': 'gjzfap1.com'},
                # {'host_ip': '172.16.153.131', 'host_name': 'gjzfap2.com'}]

        un_gorup_qst = models.InventoryHosts.objects.filter(group__group_name=None
                                                            ).annotate(host_name=F('host__hostname')
                                                                       ).values('id', 'host_name')

        # <QuerySet [{'host_ip': '1.1.1.1', 'host_name': 'bargap3.com'},
        # {'host_ip': '9.9.9.9', 'host_name': 'bmonap1.com'}]>

        # print(un_gorup_qst)
        _dic2['un_group'] = list(un_gorup_qst)

        return _dic2


if __name__ == '__main__':
    gh = GetInventoryHosts()
    print(gh.mathode2())
