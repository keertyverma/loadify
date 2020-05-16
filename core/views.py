from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from .forms import *
from .models import *


class Home(TemplateView):
    template_name = 'home.html'


class ProductListView(ListView):
    model = ProductModel
    template_name = 'products/list.html'
    context_object_name = 'products'


class CreateProductView(CreateView):
    model = ProductModel
    form_class = ProductForm
    success_url = reverse_lazy('product_list')
    template_name = 'products/create.html'
