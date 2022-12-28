from asyncio.windows_events import NULL
from ctypes.wintypes import PLARGE_INTEGER
import datetime
from email import header
import logging

import requests
from django.http import HttpResponseRedirect, JsonResponse, request, response
from django.shortcuts import render
from django.template.response import TemplateResponse

from common.views import BaseView


logger = logging.getLogger(__name__)


# Create your views here.
def login(request):
    """登录页面，使用模板渲染"""
    return render(request, 'login.html')

class ApiLogin(BaseView):
    def post(self, request):
        """点击登录按钮时调用此接口，通过比赛接口/api/auth/token验证用户名和密码，获取token，同时开机（开机是不得已为之，未来需要分离出来）"""
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 通过token接口验证用户名和密码
        api_json = self.api_login(request, username, password)
        logger.debug('登录获取token结果为：%s', api_json)   
        if api_json.get('code') != 0 or not api_json.get('token'):
            # 登录失败展示报错信息
            return render(request, 'login.html', {'message': api_json['message']})
        token = api_json.get('token')

        # 远程链接
        url = 'https://119.36.235.228:10110/api/instances/connection'
        headers = {'Authorization': 'Bearer ' + token}
        request_json = {
            "instance_id": "46e5999f-7b14-40e4-844a-cff43ae913df",
            "username": username         
        }
        r = requests.post(url=url, json=request_json, headers=headers, verify=False)
        response_json = r.json()
        if response_json['code'] == 0:
            # access_url = response_json['instance']["connect"]["access_url"]
            print(f'链接成功，{response_json}')
        else:
            print(f'连接失败{response_json}')

        # # 开机
        # url = 'https://119.36.235.228:10110/api/instances/start'
        # headers = {'Authorization': 'Bearer ' + token}
        # request_json = {
        #     "instance_ids": ["64eae7ed-b32f-4450-9697-b5c075103d48"],
        #     "is_edaas": True            
        # }
        # r = requests.post(url=url, json=request_json, headers=headers, verify=False)
        # response_json = r.json()
        # if response_json['code'] == 0:
        #     print(f'开机成功，{response_json}')
        # else:
        #     print(f'开机失败，{response_json}')

        # 登录成功跳转到配额展示页面
        response = HttpResponseRedirect('/website/quotas/')
        response.set_cookie('sessionid', request.session.session_key)
        return response



class ProductsView(BaseView):
    def get(self, request):
        api_json = self.api_get(request, '/products_folder')
        logger.debug('获取产品目录结果为：%s', api_json)
        products_folder = api_json['products_folder']

        api_json = self.api_get(request, '/products')
        logger.debug('获取产品列表结果为：%s', api_json)
        products = api_json['products']

        return render(request, 'products.html', {'products_folder': products_folder, 'products': products})


class QuotasView(BaseView):
    def get(self, request):
        api_json = self.api_get(request, '/quotas/current-user')
        return render(request, 'quotas.html', {'result': api_json['result']})


class DesktopsView(BaseView):
    def get(self, request):
        api_json = self.api_get(request, '/instances')
        logger.debug('获取服务桌面结果为：%s', api_json)
        desktops = api_json['result']

        api_json = self.api_get(request, '/quotas/current-user')
        quotas = api_json['result']['quotas']

        api_json = self.api_get(request, '/products')
        products = api_json['products']

        return render(request, 'desktops.html', {'desktops': desktops, 'products': products, 'quotas': quotas})


class ApiDesktopsView(BaseView):
    def post(self, request):
        display_name = request.POST.get('display_name')
        start_ip = request.POST.get('start_ip')
        description = request.POST.get('description')
        product_id = request.POST.get('product_id')
        memory_mb = request.POST.get('memory_mb')
        vcpu = request.POST.get('vcpu')
        system_gb = request.POST.get('system_gb')
        local_gb = request.POST.get('local_gb')

        api_json = self.api_post(request, '/instances', {
            'display_name': display_name,
            'start_ip': start_ip,
            'description': description,
            'product_id': product_id,
            'memory_mb': memory_mb,
            'vcpu': vcpu,
            'system_gb': system_gb,
            'local_gb': local_gb,
            'expand_enabled': False
        })
        logger.debug('创建服务桌面结果为：%s', api_json)
        return JsonResponse(api_json)
