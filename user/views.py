import json
import logging

import requests
from django.http import JsonResponse

from common.views import BaseView

logger = logging.getLogger(__name__)


# Create your views here.
class LoginView(BaseView):
    def post(self, request):
        """通过token接口验证用户名和密码，验证成功的话设置cookie"""
        request_json = json.loads(request.body)
        username = request_json.get('username')
        password = request_json.get('password')

        # 通过token接口验证用户名和密码
        response = requests.post(self.api_url + '/auth/token', json={'username': username, 'password': password})
        response_json = response.json()
        if response_json.get('code') != 0:
            return JsonResponse(response_json, status=400)

        request.session['username'] = username
        request.session['token'] = response_json.get('token')
        request.session['refresh_token'] = response_json.get('refresh_token')
        response = JsonResponse(response_json)
        response.set_cookie('sessionid', request.session.session_key)

        return JsonResponse({'code': 0, 'message': '登录成功'})


class LogoutView(BaseView):
    def post(self, request):
        """退出登录，清除cookie和session"""
        logger.debug('session: %s', request.session.items())
        request.session.clear()
        response = JsonResponse({'code': 0, 'message': '退出登录成功'})
        response.delete_cookie('sessionid')
        return response