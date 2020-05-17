
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
    path('products/update/<pk>', views.UpdateProductView.as_view(),
         name='product_update'),

    path('products/upload', views.CreateProductUploadView.as_view(),
         name='product_upload'),
    path('products/upload/list', views.ProductUploadListView.as_view(),
         name='product_upload_list'),

    path('products/webhook', views.CreateWebhookView.as_view(),
         name='create_webhook'),
    path('products/webhook/list', views.WebhookListView.as_view(),
         name='webhook_list'),
    path('products/webhook/update/<pk>', views.UpdateWebhookView.as_view(),
         name='webhook_update'),

]
