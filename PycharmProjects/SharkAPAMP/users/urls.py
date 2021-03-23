
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
urlpatterns = [
    url(r'^user_login/$', views.LoginView.as_view(), name='user_login'),
    url(r'user_logout/$', views.MyLogoutView.as_view(), name='user_logout'),
    url(r'^group.html/$', views.GroupListView.as_view(), name='group'),
    url(r'^group_of_users.html/(\d+)/$', views.GroupOfUsersList.as_view(), name='get_group_of_users'),

]
