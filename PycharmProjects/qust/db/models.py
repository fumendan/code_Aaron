from django.db import models
from django.utils import timezone


# Create your models here.

class ServerMachine(models.Model):
    server_ip = models.GenericIPAddressField(verbose_name='IP地址', null=True,blank=True)
    hostname = models.CharField(verbose_name='主机名', max_length=128, unique=True)
    os = models.CharField(verbose_name='系统版本', max_length=128)
    cpu_kernel = models.CharField(verbose_name='CPU内核版本', max_length=128)
    mem_total = models.FloatField(verbose_name='total内存GB', null=True, blank=True)
    mem_used = models.FloatField(verbose_name='used内存GB', null=True, blank=True)
    disk_capacity = models.FloatField(verbose_name='磁盘容量GB', null=True, blank=True)

    latest_date = models.DateTimeField(verbose_name='更新时间', default=timezone.now, null=True)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = '服务器表'
        db_table = 'server_machine'

    def __str__(self):
        return '服务器：{}'.format(self.hostname)


class UserProfile(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=128)
    password = models.CharField(verbose_name='密码', max_length=128)
    email = models.EmailField(verbose_name='邮箱', max_length=128)
    phone = models.CharField(verbose_name='电话', max_length=11)

    class Meta:
        db_table = 'user_profile'
        verbose_name_plural = '用户表'

    def __str__(self):
        return '{}'.format(self.username)
