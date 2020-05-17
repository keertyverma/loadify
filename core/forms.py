from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ('sku_orig', 'name', 'description', 'is_active')

    def clean_sku_orig(self):
        sku = self.cleaned_data['sku_orig'].lower()
        if ProductModel.objects.filter(sku=sku).exists():
            raise forms.ValidationError("This SKU already exists")
        return sku


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ('sku_orig', 'name', 'description', 'is_active')
        widgets = {
            'sku_orig': forms.TextInput(attrs={'disabled': True}),
        }


class ProductDeleteForm(forms.ModelForm):
    class Meta:
        model = ProductTruncateModel
        fields = ()


class ProductUploadForm(forms.ModelForm):
    class Meta:
        model = ProductUploadModel
        fields = ('path',)


class WebhookForm(forms.ModelForm):
    class Meta:
        model = WebhookModel
        fields = ('name', 'url', 'is_active')
