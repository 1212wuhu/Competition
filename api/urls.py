from . import views
from django.urls import path


urlpatterns = [
    path('instances/', views.InstancesView.as_view()),
    path('instances/connection/', views.InstanceConnectionView.as_view()),
    path('instances/start/', views.InstanceStartView.as_view()),
    path('products/', views.ProductsView.as_view()),
    path('products_folder/', views.ProductsFolderView.as_view()),
    path('quotas/current-user/', views.QuotasView.as_view()),
]
