from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.views.generic import View


# Create your views here.

def index(request):
    return render(request, 'cmdb_login.html')


def users_login(request):
    v_user = 'aaron'
    v_password = '1'
    if request.method == "POST":
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        if user_name == v_user and password == v_password:
            # return render(request, 'dash_board.html')
            return redirect('/server/dashboard/')
        else:
            return redirect('/')
    else:
        return redirect('/')


class UserManage(View):
    def get(self, request):
        return render(request, 'user_manage.html')


class GroupManage(View):
    def get(self, request):
        return render(request, 'group_manage.html')

