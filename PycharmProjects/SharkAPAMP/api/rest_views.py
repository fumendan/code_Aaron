#!/usr/bin/env python
# -*- coding:utf-8 -*-

#----------------------- 基本使用开始 -------------------------
from db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from api.serializersa import ServerSerializer
class ServersListView(APIView):
    '''List all servers'''

    def get(self, request, format=None):
        servers = models.Server.objects.all()
        servers_serializer = ServerSerializer(servers, many=True)
        return Response(servers_serializer.data)

    def post(self, request, format=None):
        serializer = ServerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#---------------------- 基本使用结束 ---------------------------


####################### 适当进阶开始 #######################
# from db import models
# from .serializers import ServerSerializer
# from rest_framework import mixins
# from rest_framework import generics
#
#
# class ServersListView(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = models.Server.objects.all()
#     serializer_class = ServerSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
"""
构建视图GenericAPIView，并添加ListModelMixin和CreateModelMixin。

基类提供核心功能，mixin类提供.list()和.create()操作。
然后，我们明确地将方法get和post方法绑定到适当的操作。
"""
#-------------------------------------------------------

####################### 使用通用的基于类的视图
# from db import models
# from .serializers import ServerSerializer
# from rest_framework import generics
#
#
# class ServersListView(generics.ListCreateAPIView):
#     queryset = models.Server.objects.all()
#     serializer_class = ServerSerializer


# class ServersDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Server.objects.all()
#     serializer_class = ServerSerializer




######################  终极方案  #####################
# from db import models
# from .serializersa import ServerSerializer
from rest_framework import viewsets


# class ServerListView(viewsets.ModelViewSet):
#     """
#     服务器资源列表
#     """
#     queryset = models.Server.objects.all()
#     serializer_class = ServerSerializer