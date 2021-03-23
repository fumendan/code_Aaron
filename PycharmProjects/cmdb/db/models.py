from django.db import models
from django.utils import timezone


# Create your models here.

class UsersProfile(models.Model):
    username = models.CharField('用户名', max_length=128)
    password = models.CharField('密码', max_length=128)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)  # unique 不允许重复
    mobile = models.CharField('手机', max_length=11)

    class Meta:
        db_table = 'user_profile'
        verbose_name_plural = '用户表'

    def __str__(self):
        return '{}'.format(self.username)


class UserGroup(models.Model):
    """
    用户组
    ID   名称
     1   组A
     2   组B
     3   组C
    -------------
    用户组和用户关系表
    组ID    用户ID
     1       1
     1       2
     2       1
     2       3
    """
    name = models.CharField(verbose_name='组名', max_length=32, unique=True)
    users = models.ManyToManyField('UsersProfile', verbose_name='用户成员')

    class Meta:
        verbose_name_plural = "用户组表"
        db_table = "user_group"

    def __str__(self):
        return self.name


# class Asset(models.Model):
#     """
#     资产信息表，所有资产公共信息（交换机，服务器，防火墙等）
#     """
#     device_type_choices = (
#         (1, '服务器'),
#         (2, '路由器'),
#         (3, '交换机'),
#         (4, '防火墙'),
#     )
#     device_status_choices = (
#         (1, '上架'),
#         (2, '在线'),
#         (3, '离线'),
#         (4, '下架'),
#     )
#
#     device_type_id = models.IntegerField(choices=device_type_choices, default=1)
#     device_status_id = models.IntegerField(choices=device_status_choices, default=1)
#     # 多个资产可以放在一个机柜中，也就是多对一，
#     # 即：此字段会有相同的值
#     cabinet_id = models.ForeignKey('Cabinet', verbose_name='所属机柜', max_length=30, null=True, blank=True)
#     idc = models.ForeignKey('IDC', verbose_name='IDC机房', null=True, blank=True)
#     latest_date = models.DateField(verbose_name='更新时间', null=True, blank=True)
#     create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
#
#     class Meta:
#         verbose_name = "资产表"
#         verbose_name_plural = verbose_name
#         db_table = 'asset'
#
#     def __str__(self):
#         return "{}-{}-{}".format(self.idc.name, self.device_type_id, self.device_status_id)
#
#
# class IDC(models.Model):
#     name = models.CharField(verbose_name='机房', max_length=128)
#     city = models.CharField(verbose_name='城市', max_length=32)
#     address = models.CharField(verbose_name='地址', max_length=256)
#
#     class Meta:
#         verbose_name_plural = '机房表'
#         db_table = "idc"
#
#     def __str__(self):
#         return self.name
#
#
# class Cabinet(models.Model):
#     name = models.CharField(verbose_name='机柜编号', max_length=128)
#     cab_lever = models.CharField(verbose_name='U 数', max_length=2)  # 机柜总共几层
#     idc = models.ForeignKey('IDC', verbose_name='所属机房', null=True, blank=True)
#
#     class Meta:
#         verbose_name_plural = '机柜表'
#         db_table = "cabinet"
#
#     def __str__(self):
#         return self.name
#
#
# class Server(models.Model):
#     # 每个服务器都和资产表一一对应
#     asset = models.OneToOneField('Asset', verbose_name='对应资产', null=True, blank=True)
#     hostname = models.CharField(verbose_name='主机名', max_length=128, unique=True)
#     sn = models.CharField(verbose_name='SN号', max_length=64, db_index=True)  # 为此字段创建索引
#     manage_ip = models.GenericIPAddressField(verbose_name='管理IP', null=True, blank=True)
#     latest_date = models.DateTimeField(verbose_name='更新时间', default=timezone.now, null=True)
#     create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
#     """
#     auto_now=True 每次更新，日期自动存为当前时间，并且在 Admin 管理中，此字段将不支持修改
#     default 是同时支持后台管理时间并且回自动存为当前时间
#     """
#
#     class Meta:
#         verbose_name = "服务器表"
#         verbose_name_plural = verbose_name
#         db_table = 'server'
#
#     def __str__(self):
#         return self.hostname
#
#
# class Disk(models.Model):
#     """
#     硬盘信息
#     """
#     slot = models.CharField(verbose_name='插槽位', max_length=8)
#     model = models.CharField(verbose_name='磁盘型号', max_length=32)
#     capacity = models.FloatField(verbose_name='磁盘容量GB')
#     pd_type = models.CharField(verbose_name='接口类型', max_length=32)
#     server_obj = models.ForeignKey('Server', related_name='disk', verbose_name='所属服务器')
#
#     class Meta:
#         verbose_name = "硬盘表"
#         verbose_name_plural = verbose_name
#         db_table = 'disk'
#
#     def __str__(self):
#         return self.slot
# class NIC(models.Model):
#     """
#     网卡信息
#     """
#     name = models.CharField(verbose_name='网卡名称', max_length=128)
#     hwaddr = models.CharField(verbose_name='网卡mac地址', max_length=64)
#     netmask = models.CharField(verbose_name='掩码', max_length=64)
#     ipaddrs = models.CharField(verbose_name='ip地址', max_length=256)
#     up = models.BooleanField(default=False)
#     server_obj = models.ForeignKey('Server', related_name='nic', verbose_name='所属服务器')
#
#     class Meta:
#         verbose_name = "网卡表"
#         verbose_name_plural = verbose_name
#         db_table = 'nic'
#
#     def __str__(self):
#         return self.name
#
# class Memory(models.Model):
#     """
#     内存信息
#     """
#     slot = models.CharField(verbose_name='插槽位', max_length=32)
#     manufacturer = models.CharField(verbose_name='制造商', max_length=32, null=True, blank=True)
#     model = models.CharField(verbose_name='型号', max_length=64)
#     capacity = models.FloatField(verbose_name='容量', null=True, blank=True)
#     sn = models.CharField(verbose_name='内存SN号', max_length=64, null=True, blank=True)
#     speed = models.CharField(verbose_name='速度', max_length=16, null=True, blank=True)
#
#     server_obj = models.ForeignKey('Server', related_name='memory', verbose_name='所属服务器')
#
#     class Meta:
#         verbose_name = "内存表"
#         verbose_name_plural = verbose_name
#         db_table = 'memory'
#
#     def __str__(self):
#         return self.slot

class Server(models.Model):
    """
    服务器信息
    model_name    CPU 型号
    physical_count   物理 CPU 个数
    physical_cores     每颗物理 CPU 的核心数
    processor_cores_count     CPU 总逻辑核心数

    'machine': 硬件平台,
    'os_name': 操作系统名称,
    'os_version': 操纵系统发行版本,
    'hostname': 主机名,
    'kernel': 内核名称、版本、发行时间
    """
    # asset = models.OneToOneField('Asset', verbose_name='对应资产', null=True, blank=True)

    hostname = models.CharField(verbose_name='主机名', max_length=128, unique=True)
    sn = models.CharField(verbose_name='SN号', max_length=64, db_index=True)  # 为此字段创建索引
    manufacturer = models.CharField(verbose_name='制造商', max_length=64, null=True, blank=True)
    model = models.CharField(verbose_name='型号', max_length=64, null=True, blank=True)
    manage_ip = models.GenericIPAddressField(verbose_name='管理IP', null=True, blank=True)
    machine = models.CharField(verbose_name='硬件平台', max_length=16, null=True, blank=True)
    os_name = models.CharField(verbose_name='系统名称', max_length=16, null=True, blank=True)
    os_version = models.CharField(verbose_name='系统版本', max_length=64, null=True, blank=True)
    kernel = models.CharField(verbose_name='内核信息', max_length=128, null=True, blank=True)
    model_name = models.CharField(verbose_name='CPU型号', max_length=128, null=True, blank=True)
    cpu_type = models.CharField(verbose_name='CPU 架构', max_length=16, null=True, blank=True)
    physical_count = models.IntegerField(verbose_name='CPU物理个数', null=True, blank=True)
    physical_cores = models.IntegerField(verbose_name='每颗 CPU 核心数', null=True, blank=True)
    processor_cores_count = models.IntegerField(verbose_name='CPU 总逻辑核心数', null=True, blank=True)

    latest_date = models.DateTimeField(verbose_name='更新时间', default=timezone.now, null=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    """
    auto_now=True 每次更新，日期自动存为当前时间，并且在 Admin 管理中，此字段将不支持修改
    default
    """

    class Meta:
        verbose_name = "服务器表"
        verbose_name_plural = verbose_name
        db_table = 'server'

    def __str__(self):
        return self.hostname


class Disk(models.Model):
    """
    硬盘信息
    """
    slot = models.CharField(verbose_name='插槽位', max_length=8)
    model = models.CharField(verbose_name='磁盘型号', max_length=32)
    capacity = models.FloatField(verbose_name='磁盘容量GB')
    pd_type = models.CharField(verbose_name='接口类型', max_length=32)
    server_obj = models.ForeignKey('Server', related_name='disk', verbose_name='所属服务器')

    class Meta:
        verbose_name = "硬盘表"
        verbose_name_plural = verbose_name
        db_table = 'disk'

    def __str__(self):
        return self.slot


class NIC(models.Model):
    """
    网卡信息
    """
    name = models.CharField(verbose_name='网卡名称', max_length=128)
    hwaddr = models.CharField(verbose_name='网卡mac地址', max_length=64)
    netmask = models.CharField(verbose_name='掩码', max_length=64)
    ipaddrs = models.CharField(verbose_name='ip地址', max_length=256)
    up = models.BooleanField(default=False)
    server_obj = models.ForeignKey('Server', related_name='nic', verbose_name='所属服务器')

    class Meta:
        verbose_name = "网卡表"
        verbose_name_plural = verbose_name
        db_table = 'nic'

    def __str__(self):
        return self.name


class Memory(models.Model):
    """
    内存信息
    """
    slot = models.CharField(verbose_name='插槽位', max_length=32)
    manufacturer = models.CharField(verbose_name='制造商', max_length=32, null=True, blank=True)
    model = models.CharField(verbose_name='型号', max_length=64)
    capacity = models.FloatField(verbose_name='容量', null=True, blank=True)
    sn = models.CharField(verbose_name='内存SN号', max_length=64, null=True, blank=True)
    speed = models.CharField(verbose_name='速度', max_length=16, null=True, blank=True)

    server_obj = models.ForeignKey('Server', related_name='memory', verbose_name='所属服务器')

    class Meta:
        verbose_name = "内存表"
        verbose_name_plural = verbose_name
        db_table = 'memory'

    def __str__(self):
        return self.slot


class AssetChangLog(models.Model):
    """
    服务器变更记录,creator为空时，表示是资产汇报的数据。
    """
    server_obj = models.ForeignKey('Server', related_name='ar')
    content = models.TextField(verbose_name='变更内容', null=True, blank=True)
    operator = models.ForeignKey('UsersProfile', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "资产变更日志表"
        db_table = 'asset_change_log'

    def __str__(self):
        return self.server_obj.hostname
