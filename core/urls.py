
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),

    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/create/', views.CreateProductView.as_view(),
         name='product_create'),
    path('products/update/<sku>', views.CreateProductView.as_view(),
         name='product_update'),
]
