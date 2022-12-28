from . import views
from django.urls import path


urlpatterns = [
    # 以下url，带api前缀的是api接口，不带api前缀的是页面
    # 登录
    path('login/', views.login),
    path('api/login/', views.ApiLogin.as_view()),

    # 产品目录，产品列表
    path('products/', views.ProductsView.as_view()),

    # 用户配额
    path('quotas/', views.QuotasView.as_view()),

    # 服务桌面
    path('desktops/', views.DesktopsView.as_view()),
    path('api/desktops/', views.ApiDesktopsView.as_view()),
]
