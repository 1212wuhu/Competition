import datetime

import requests

# 调用比赛的token接口，输入用户名和密码，获取token用来调用后续其他接口
def login(username, password):
    # 请求的url地址见接口文档
    url = 'http://test-api.os-easy.com:8000/api/auth/token'
    # 请求的参数见接口文档
    request_json = {'username': username, 'password': password}
    # 发送请求
    r = requests.post(url, json=request_json)
    # 获取返回的json数据
    response_json = r.json()
    if response_json['code'] == 0:
        # 获取token
        token = response_json['token']
        print(f'登录成功，token为：{token}')
        return token
    else:
        print(f'登录失败，错误信息为：{response_json["message"]}')
        return None

# 调用后台比赛接口的工具类，需要传入token和请求的url地址
def api_get(url, token):
    # url地址前面部分都是一样的，只是最后的path有区别
    url_prefix = 'http://test-api.os-easy.com:8000/api'
    url = url_prefix + url
    # 请求的http头部信息要带上token，注意Bearer和token之间有空格
    headers = {'Authorization': 'Bearer ' + token}

    # 发送请求
    r = requests.get(url, headers=headers)
    # 获取返回的json数据
    response_json = r.json()
    if response_json['code'] == 0:
        # 获取返回的数据
        print(f'获取数据成功，数据为：{response_json}')
        return response_json
    else:
        print(f'获取数据失败，错误信息为：{response_json["message"]}')
        return None

# 获取当前用户的配额信息
def get_quota(token):
    response_json = api_get('/quotas/current-user', token)
    if response_json:
        # 获取配额信息
        quota = response_json['result']['quotas']
        print(f'获取配额信息成功，配额信息为：{quota}')

# 获取产品目录
def get_products_folder(token):
    response_json = api_get('/products_folder', token)
    if response_json:
        # 获取产品目录信息
        products_folder = response_json['products_folder']
        print(f'获取产品目录信息成功，产品目录信息为：{products_folder}')

# 获取产品列表
def get_products(token):
    response_json = api_get('/products', token)
    if response_json:
        # 获取产品列表信息
        products = response_json['products']
        print(f'获取产品列表信息成功，产品列表信息为：{products}')

# 创建服务桌面
def create_service_desktop(token):
    # 请求的url地址见接口文档
    url = 'http://test-api.os-easy.com:8000/api/instances'
    # http头
    headers = {'Authorization': 'Bearer ' + token}
    # 请求的参数见接口文档
    # {
    #     "display_name": "rh-test",
    #     "start_ip": "172.17.28.15",
    #     "description": "新建的桌面",
    #     "product_id": 1,
    #     "memory_mb": 6,
    #     "vcpu": 4,
    #     "system_gb": 20,
    #     "local_gb": 0,
    #     "expand_enabled": false
    # }
    request_json = {
        'display_name': f'test-{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}',
        'start_ip': '192.168.0.110',
        'description': '新建的桌面',
        'product_id': 1,
        'memory_mb': 1024,  # 建议值
        'vcpu': 1,  # 建议值
        'system_gb': 20,  # 建议值
        'local_gb': 0,
        'expand_enabled': False  # 只有一个屏幕，防止后续获取桌面画面时拿不到主屏幕（黑屏）
    }

    # 发送请求
    r = requests.post(url, json=request_json, headers=headers)
    # 获取返回的json数据
    response_json = r.json()
    if response_json['code'] == 0:
        # 获取返回的数据
        print(f'创建服务桌面成功，数据为：{response_json}')
        return response_json
    else:
        print(f'创建服务桌面失败，错误信息为：{response_json["message"]}')
        return None