from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from datetime import datetime

import django_filters

from .forms import *
from .models import *


class Home(TemplateView):
    template_name = 'home.html'


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains')
    is_active = django_filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = ProductModel
        fields = ('name', 'is_active')


class ProductListView(ListView):
    model = ProductModel
    template_name = 'products/list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


class CreateProductView(CreateView):
    model = ProductModel
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    template_name = 'products/create.html'


class UpdateProductView(UpdateView):
    model = ProductModel
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    template_name = 'products/update.html'

    def form_valid(self, form):
        form.instance.updated_at = datetime.utcnow()
        return super(UpdateProductView, self).form_valid(form)


class ProductUploadListView(ListView):
    model = ProductUploadModel
    template_name = 'product_uploads/list.html'
    context_object_name = 'products_upload'


class CreateProductUploadView(CreateView):
    model = ProductUploadModel
    form_class = ProductUploadForm
    success_url = reverse_lazy('product_upload_list')
    template_name = 'product_uploads/upload.html'


class WebhookListView(ListView):
    model = WebhookModel
    template_name = 'webhooks/list.html'
    context_object_name = 'webhooks'


class CreateWebhookView(CreateView):
    model = WebhookModel
    form_class = WebhookForm
    success_url = reverse_lazy('webhook_list')
    template_name = 'webhooks/create.html'


class UpdateWebhookView(UpdateView):
    model = WebhookModel
    form_class = WebhookForm
    success_url = reverse_lazy('webhook_list')
    template_name = 'webhooks/update.html'

    def form_valid(self, form):
        form.instance.updated_at = datetime.utcnow()
        return super(UpdateWebhookView, self).form_valid(form)
