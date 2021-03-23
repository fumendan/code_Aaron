from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

"""
null¶
Field.null¶
如果True，Django将像NULL数据库中那样存储空值。默认是False。

避免使用null基于字符串的字段，如 CharField和TextField。
如果一个基于字符串的字段有 null=True，那就意味着它有两个可能的值：“无数据” NULL和空字符串。
在大多数情况下，为“无数据”提供两个可能的值是多余的，Django约定是使用空字符串，而不是 NULL。
有一个例外是，当一个CharField都有，unique=True 并blank=True设置。在这种情况下，null=True需要避免在使用空值保存多个对象时出现唯一的约束违规。

对于基于字符串和非基于字符串的字段，您还需要设置blank=True是否希望允许表单中的空值，因为该 null参数仅影响数据库存储（请参阅参考资料blank）。

blank
Field.blank
如果True，该字段被允许为空白。默认是False。

请注意，这不同于null。null纯粹是与数据库相关的，而blank与验证相关。
如果一个字段有blank=True，表单验证将允许输入一个空值。
如果一个字段有blank=False，该字段将是必需的。
"""


class UsersProfile(AbstractUser):
    password = models.CharField('密码', max_length=128)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    phone = models.CharField('座机', max_length=11)
    mobile = models.CharField('手机', max_length=11)

    class Meta:
        verbose_name_plural = "用户表"
        db_table = 'users_profile'


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


class Department(models.Model):
    """
    部门
    """
    name = models.CharField(verbose_name='部门', max_length=64, unique=True)  # 应用一处，销售1,2
    supervisor = models.ForeignKey('UsersProfile', verbose_name='负责人', null=True)  # 部门负责人

    class Meta:
        verbose_name = "部门表"
        verbose_name_plural = verbose_name
        db_table = "department"

    def __str__(self):
        return self.name


class AppClass(models.Model):
    """
    应用类别/业务线
    """
    name = models.CharField(verbose_name='应用名称', max_length=64, unique=True)  # 国际支付前置，逻辑集中
    business = models.ForeignKey('Department', verbose_name='部门')
    manager = models.ForeignKey('UserGroup', verbose_name='运维人员')  # 运维管理人员

    class Meta:
        verbose_name = "应用分类表"
        verbose_name_plural = verbose_name
        db_table = "app_class"

    def __str__(self):
        return self.name


class IDC(models.Model):
    name = models.CharField(verbose_name='机房', max_length=128)
    city = models.CharField(verbose_name='城市', max_length=32)
    address = models.CharField(verbose_name='地址', max_length=256)

    class Meta:
        verbose_name_plural = '机房表'
        db_table = "idc"

    def __str__(self):
        return self.name


class Cabinet(models.Model):
    name = models.CharField(verbose_name='机柜编号', max_length=128)
    cab_lever = models.CharField(verbose_name='U 数', max_length=2)  # 机柜总共几层
    idc = models.ForeignKey('IDC', verbose_name='所属机房', null=True, blank=True)

    class Meta:
        verbose_name_plural = '机柜表'
        db_table = "cabinet"

    def __str__(self):
        return self.name


class Asset(models.Model):
    """
    资产信息表，所有资产公共信息（交换机，服务器，防火墙等）
    """
    device_type_choices = (
        (1, '服务器'),
        (2, '路由器'),
        (3, '交换机'),
        (4, '防火墙'),
    )
    device_status_choices = (
        (1, '上架'),
        (2, '在线'),
        (3, '离线'),
        (4, '下架'),
    )

    device_type_id = models.IntegerField(choices=device_type_choices, default=1)
    device_status_id = models.IntegerField(choices=device_status_choices, default=1)

    cabinet_num = models.ForeignKey('Cabinet', verbose_name='机柜号', max_length=30, null=True, blank=True)
    cabinet_order = models.CharField(verbose_name='机柜中序号', max_length=30, null=True, blank=True)

    idc = models.ForeignKey('IDC', verbose_name='IDC机房', null=True, blank=True)
    department = models.ForeignKey('Department', verbose_name='所属部门', null=True, blank=True)
    app_class = models.ForeignKey('AppClass', verbose_name='所属应用', null=True, blank=True)
    latest_date = models.DateField(verbose_name='更新时间', null=True, blank=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name = "资产表"
        verbose_name_plural = verbose_name
        db_table = 'asset'

    def __str__(self):
        return "{}-{}-{}".format(self.idc.name, self.cabinet_num, self.cabinet_order)


class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset', null=True, blank=True)
    device_name = models.CharField(verbose_name='设备名称', max_length=128, blank=True, null=True)
    management_ip = models.CharField(verbose_name='管理IP', max_length=64, blank=True, null=True)
    vlan_ip = models.CharField('VlanIP', max_length=64, blank=True, null=True)
    intranet_ip = models.CharField(verbose_name='内网IP', max_length=128, blank=True, null=True)
    sn = models.CharField('SN号', max_length=64, unique=True)
    manufacture = models.CharField(verbose_name='制造商', max_length=128, null=True, blank=True)
    model = models.CharField(verbose_name='型号', max_length=128, null=True, blank=True)
    port_num = models.SmallIntegerField(verbose_name='端口个数', null=True, blank=True)
    device_detail = models.CharField(verbose_name='设置详细配置', max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "网络设备"
        verbose_name_plural = verbose_name
        db_table = 'network_device'

    def __str__(self):
        return "{}-{}".format(self.device_name, self.sn)


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
    asset = models.OneToOneField('Asset', verbose_name='对应资产', null=True, blank=True)

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


class ModuleInfo(models.Model):
    type_chioces = [(0, "-------"), (1, "ansible"), (2, "shell"), (3, "salt")]
    lang_chioces = [(0, "-------"), (1, "python"), (2, "shell"), (3, "其他")]
    module_name = models.SlugField("模块名", max_length=64)
    module_type = models.IntegerField('模块类型',
                                      choices=type_chioces,
                                      )
    module_lang = models.IntegerField('开发语言',
                                      choices=lang_chioces,
                                      )
    module_info = models.TextField('模块概述')
    module_path = models.FilePathField('模块路径', null=True, blank=True)
    latest_date = models.DateTimeField('更新时间', auto_now=timezone.now(), null=True)
    create_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Mata:
        db_table = "module_info"
        verbose_name_plural = "模块信息表"
        # 联合唯一索引
        unique_together = ("module_name", "module_type")

    def __str__(self):
        return "{}--{}--{}".format(self.module_name, self.get_module_type_display(), self.get_module_lang_display())


class InventoryGroups(models.Model):
    group_name = models.CharField(verbose_name='主机组名', max_length=64)
    Summary = models.TextField(verbose_name="主机组概述", max_length=255)
    parent_group = models.ForeignKey('self', verbose_name="父级组", null=True, blank=True)
    latest_date = models.DateTimeField('更新时间', auto_now=timezone.now(), null=True)
    create_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'inventory_groups'
        verbose_name_plural = 'Ansible 主机组表'

    def __str__(self):
        return "{}".format(self.group_name)


class InventoryHosts(models.Model):
    host = models.OneToOneField('Server', verbose_name='主机名')
    group = models.ManyToManyField('InventoryGroups', verbose_name='主机组', null=True, blank=True)
    latest_date = models.DateTimeField('更新时间', auto_now=timezone.now(), null=True)
    create_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'inventory_hosts'
        verbose_name_plural = 'Ansible 主机表'

    def __str__(self):
        return "{}".format(self.host)


class VariableInfo(models.Model):
    key = models.CharField('变量名', max_length=128)
    values = models.CharField('变量值', max_length=255)
    groups = models.ManyToManyField('InventoryGroups', verbose_name='归属组', null=True, blank=True)
    hosts = models.ManyToManyField('InventoryHosts', verbose_name='归属主机', null=True, blank=True)
    latest_date = models.DateTimeField('更新时间', auto_now=timezone.now(), null=True)
    create_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'variable_info'
        verbose_name_plural = '变量表'

    def __str__(self):
        return "{}--{}".format(self.key, self.values)


class ConnectionInfo(models.Model):
    auth_type_choices = ((0, 'password'), (1, 'free-key'))
    auth_type = models.IntegerField(choices=auth_type_choices, default=0)
    host = models.ManyToManyField('InventoryHosts', verbose_name='主机 ID')
    remote_user = models.CharField(verbose_name='远程登录用户名', max_length=64)
    password = models.CharField(verbose_name='登录密码', max_length=255)
    port = models.IntegerField()
    latest_date = models.DateTimeField('更新时间', auto_now=timezone.now(), null=True)
    create_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'connection_info'
        verbose_name_plural = 'SSH 连接信息表'
        unique_together = ('auth_type', 'remote_user', 'password')

    def __str__(self):
        return "{}-{}".format(self.remote_user, self.password)
