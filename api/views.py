import logging

from common.views import BaseView

logger = logging.getLogger(__name__)


# Create your views here.
class InstancesView(BaseView):
    def get(self, request):
        """获取服务桌面列表"""
        return self.api_get(request, '/instances')

    def post(self, request):
        """创建服务桌面"""
        return self.api_post(request, '/instances')


class InstanceConnectionView(BaseView):
    def post(self, request):
        """获取服务桌面连接信息"""
        return self.api_post(request, '/instances/connection')

class InstanceStartView(BaseView):
    def post(self, request):
        """服务桌面开机"""
        return self.api_post(request, '/instances/start')


class ProductsView(BaseView):
    def get(self, request):
        """获取产品列表"""
        return self.api_get(request, '/products')


class ProductsFolderView(BaseView):
    def get(self, request):
        """获取产品目录"""
        return self.api_get(request, '/products_folder')


class QuotasView(BaseView):
    def get(self, request):
        """获取用户配额"""
        return self.api_get(request, '/quotas/current-user')
