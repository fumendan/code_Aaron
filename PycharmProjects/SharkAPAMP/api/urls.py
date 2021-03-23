from django.conf.urls import url, include
from . import views
from . import rest_views
from rest_framework.routers import DefaultRouter

# api_routers = DefaultRouter()
# api_routers.register(r'servers', api_views.ServerListView)  # 注册路由

from rest_framework.documentation import include_docs_urls
from api import rest_views

urlpatterns = [
    # url('^', include(api_routers.urls)),
    # url(r'^asset.html$', views.asset),

    url(r'^servers/$', rest_views.ServersListView.as_view()),
    url(r'^docs/', include_docs_urls(title="服务器")),

]
