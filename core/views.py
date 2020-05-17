from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, FormView, RedirectView
from django.views.generic.edit import FormView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from datetime import datetime
import django_filters
from django_filters.views import FilterView
from django_eventstream import send_event
import csv
import os
from urllib import parse

from .forms import *
from .models import *
from .tasks import import_csv, trigger_webhook


class Home(TemplateView):
    template_name = 'home.html'


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains')
    is_active = django_filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = ProductModel
        fields = ('name', 'is_active')


class ProductListFilteredView(FilterView):
    model = ProductModel
    filterset_class = ProductFilter
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 10


class CreateProductView(CreateView):
    model = ProductModel
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    template_name = 'products/create.html'

    def form_valid(self, form):
        form.instance.sku = form.instance.sku_orig.lower()
        return super().form_valid(form)

    def get_success_url(self):
        trigger_webhook.delay(self.object.sku, "product_create")
        return super().get_success_url()


class UpdateProductView(UpdateView):
    model = ProductModel
    form_class = ProductUpdateForm
    success_url = reverse_lazy('product_list')
    template_name = 'products/update.html'

    def form_valid(self, form):
        form.instance.updated_at = datetime.utcnow()
        return super(UpdateProductView, self).form_valid(form)

    def get_success_url(self):
        trigger_webhook.delay(self.object.sku, "product_update")
        return super().get_success_url()


class DeleteProductView(CreateView):
    model = ProductTruncateModel
    form_class = ProductDeleteForm
    success_url = reverse_lazy('product_list')
    template_name = 'products/delete.html'

    def get_success_url(self):
        ProductModel.truncate()
        return super().get_success_url()


class TruncateProductView(RedirectView):

    permanent = False
    pattern_name = 'product_list'

    def get_redirect_url(self, *args, **kwargs):
        ProductModel.truncate()
        return super().get_redirect_url(*args, **kwargs)


class UploadProductEventView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        args = dict(parse.parse_qsl(self.request.META.get('QUERY_STRING', '')))
        send_event('upload_status', 'message', {
                   'id': args['id'], 'status': args['status'], 'count': args['count']})
        return None


class ProductUploadListView(ListView):
    model = ProductUploadModel
    template_name = 'product_uploads/list.html'
    context_object_name = 'product_uploads'


class CreateProductUploadView(CreateView):
    model = ProductUploadModel
    form_class = ProductUploadForm
    success_url = reverse_lazy('product_uploads_list')
    template_name = 'product_uploads/upload.html'

    def form_valid(self, form):
        file_object = self.request.FILES['path']
        form.instance.name = file_object.name
        form.instance.size = file_object.size
        return super(CreateProductUploadView, self).form_valid(form)

    def get_success_url(self):
        import_csv.delay(self.object.id, str(self.object.path))
        return super().get_success_url()


class WebhookListView(ListView):
    model = WebhookModel
    template_name = 'webhooks/list.html'
    context_object_name = 'webhooks'


class CreateWebhookView(CreateView):
    model = WebhookModel
    form_class = WebhookForm
    success_url = reverse_lazy('webhooks_list')
    template_name = 'webhooks/create.html'


class UpdateWebhookView(UpdateView):
    model = WebhookModel
    form_class = WebhookForm
    success_url = reverse_lazy('webhooks_list')
    template_name = 'webhooks/update.html'

    def form_valid(self, form):
        form.instance.updated_at = datetime.utcnow()
        return super(UpdateWebhookView, self).form_valid(form)
