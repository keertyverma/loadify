
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),

    path('products/', views.ProductListFilteredView.as_view(), name='product_list'),
    path('products/create/', views.CreateProductView.as_view(),
         name='product_create'),
    path('products/update/<pk>', views.UpdateProductView.as_view(),
         name='product_update'),
    path('products/delete_all', views.DeleteProductView.as_view(),
         name='product_delete_all'),

    path('products/uploads', views.ProductUploadListView.as_view(),
         name='product_uploads_list'),
    path('products/uploads/upload', views.CreateProductUploadView.as_view(),
         name='product_uploads_upload'),
    path('products/uploads/events', views.UploadProductEventView.as_view(),
         name='product_uploads_events'),


    path('products/webhooks', views.WebhookListView.as_view(),
         name='webhooks_list'),
    path('products/webhooks/create', views.CreateWebhookView.as_view(),
         name='webhooks_create'),
    path('products/webhooks/update/<pk>', views.UpdateWebhookView.as_view(),
         name='webhooks_update'),

]
