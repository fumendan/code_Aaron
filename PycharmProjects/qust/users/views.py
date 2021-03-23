from django.shortcuts import render, redirect
from django.views.generic import View
from db import models


# Create your views here.
def index(request):
    return render(request, 'login.html')


def user_login(request):
    username = request.POST.get('user_name')
    password = request.POST.get('password')
    if request.method == 'POST':
        for user_obj in models.UserProfile.objects.all():
            if user_obj.username == username and user_obj.password == password:
                return redirect('/servers/dashboard/')
        else:
            return redirect('/')
    else:
        return redirect('/')


class UserManager(View):
    def get(self, request):
        users = models.UserProfile.objects.all().values()
        return render(request, 'user_manager.html', {'users': users})


class GroupManager(View):
    def get(self, request):
        return render(request, 'group_manager.html')
