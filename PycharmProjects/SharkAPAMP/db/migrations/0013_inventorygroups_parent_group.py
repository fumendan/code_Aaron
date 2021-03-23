# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-16 05:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0012_auto_20180309_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorygroups',
            name='parent_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='db.InventoryGroups', verbose_name='父级组'),
        ),
    ]