from django.shortcuts import render, HttpResponse
from django.views.generic import View


# Create your views here.

def host_list(request, arg):
    return HttpResponse('{}'.format(arg))


# CBV class base views
class DashboardView(View):
    def get(self, request):
        server_info = {'hostname': 'xue.ido.com', 'ip': '10.18.44.52'}
        return render(request, 'dash_board.html', {'server_date': server_info})

    def post(self, request):
        pass


class Idc(View):
    def get(self, request):
        dic_data = {'idc': '这是IDC管理'}
        return render(request, 'idc.html', {'idc_data': dic_data})

    def post(self, request):
        pass


class Cabinet(View):
    def get(self, request):
        return render(request, 'cabinet.html')

    def post(self, request):
        pass
class Ser(View):
    def get(self,request):
        return render(request,'get_server.html')
class Net(View):
    def get(self,request):
        return render(request,'get_net.html')