from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  # FBV 情况下用
from django.views.generic import View, ListView
from db.models import UsersProfile, UserGroup
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView

# class MyView(LoginRequiredMixin, View):
#     login_url = '/login/'
#     redirect_field_name = 'redirect_to'


class LoginView(View):
    def get(self, request):
        return render(request, 'users/user_login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)  # 认证成功，会获取到用户对象
        print(user)
        if user:
            login(request, user)  # 向 session 中注册该用户信息
            return redirect('/')
        else:
            return render(request, 'users/user_login.html')


class MyLogoutView(LogoutView):
    #next_page = '/users/user_login/'  #  不设置，且在 settings.LOGOUT_REDIRECT_URL 设置了值，则为设置的值
    redirect_field_name = ''


class MyLoginRequiredMixin(LoginRequiredMixin):
    redirect_field_name = ''  # 跳转后不加 ?next= 字段


class GroupListView(MyLoginRequiredMixin, ListView):
    queryset = UserGroup.objects.all()
    context_object_name = 'group_list_obj'
    template_name = 'users/group.html'


class GroupOfUsersList(ListView):

    template_name = 'users/group_of_users.html'
    context_object_name = 'group_of_users_obj'

    def get_queryset(self):
        self.usergroup = get_object_or_404(UserGroup, id=self.args[0])
        return UsersProfile.objects.filter(usergroup=self.usergroup)

    # def get_context_data(self, **kwargs):