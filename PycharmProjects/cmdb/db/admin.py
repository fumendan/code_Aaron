from django.contrib import admin
from . import models


# Register your models here.
class AssetAdmin(admin.ModelAdmin):
    # 后台管理页面显示字段名
    list_display = ('cabinet_num', 'idc', 'latest_date')
    # 添加搜索功能
    search_fields = ('cabinet_num', 'idc')
    # 添加过滤功能
    list_filter = ('cabinet_num', 'idc')
    # 添加排序功能
    ordering = ('id',)


# 注册
# admin.site.register(models.Asset)
admin.site.register(models.UsersProfile)
admin.site.register(models.UserGroup)
# admin.site.register(models.IDC)
# admin.site.register(models.Cabinet)
admin.site.register(models.Server)
