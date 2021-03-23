from django.contrib import admin
from django.contrib.auth.models import Group
from db import models


class UserProfileAdmin(admin.ModelAdmin):
    pass


class ServerAdmin(admin.ModelAdmin):
    # fields = ('hostname', 'sn')
    pass


# Now register the new UserAdmin...
admin.site.register(models.UsersProfile)
# ... and, since we're not using Django's built-in permissions,
# 因为我们不使用 Django 内置的权限，所以注销掉 Group Model
admin.site.unregister(Group)

admin.site.register(models.UserGroup)
admin.site.register(models.Department)
admin.site.register(models.AppClass)
admin.site.register(models.IDC)
admin.site.register(models.Cabinet)
admin.site.register(models.Asset)
admin.site.register(models.NetworkDevice)
admin.site.register(models.Server)
admin.site.register(models.Memory)
admin.site.register(models.Disk)
admin.site.register(models.NIC)
admin.site.register(models.AssetChangLog)


admin.site.register(models.ModuleInfo)
admin.site.register(models.InventoryGroups)
admin.site.register(models.InventoryHosts)
admin.site.register(models.VariableInfo)
admin.site.register(models.ConnectionInfo)


