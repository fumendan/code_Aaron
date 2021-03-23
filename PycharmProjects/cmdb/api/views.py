import json
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def assets_story(request):
    if request.method == 'POST':
        print(type(request.body), request.body)
        asset_str = request.body.decode()
        asset_dic = json.loads(asset_str)
        print('asset_str:', asset_str)
        print('asset_dic:', asset_dic)
        return HttpResponse('汇报成功!')
