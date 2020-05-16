from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ('sku', 'name', 'description', 'is_active')
