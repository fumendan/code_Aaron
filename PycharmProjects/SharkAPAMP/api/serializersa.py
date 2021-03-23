#!/usr/bin/env python
# -*- coding:utf-8 -*-
from rest_framework import serializers


class ServerSerializer(serializers.Serializer):
    hostname = serializers.CharField(max_length=128)
    sn = serializers.CharField(max_length=64)
    manufacturer = serializers.CharField(max_length=64)


######################  终极方案  #####################
# from rest_framework import serializers
# from db import models

# class ServerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Server
#         fields = ('id', 'asset', 'hostname', 'sn')


