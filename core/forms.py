from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ('sku', 'name', 'description', 'is_active')


class ProductUploadForm(forms.ModelForm):
    class Meta:
        model = ProductUploadModel
        fields = ('name', 'path', 'total_rows', 'processed_rows')


class WebhookForm(forms.ModelForm):
    class Meta:
        model = WebhookModel
        fields = ('name', 'path')
