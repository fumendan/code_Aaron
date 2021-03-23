"""SharkAPAMP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^dash_board.html/$', views.dash_board, name='dash_board'),
    url(r'^asset/$', views.AssetListView.as_view(), name='asset'),
    url(r'^idc.html/$', views.IdcView.as_view(), name='idc'),
    url(r'^host_detail.html/(\d+)/$', views.HostDetailView.as_view(), name='host'),
    url(r'^business.html/$', views.BusinessView.as_view(), name='business'),
    url(r'^department.html/$', views.DepartmentList.as_view(), name='department'),
    url(r'^get_change_info.html/$', views.get_change),

]
