from django.db import models
from django.conf import settings
from django.utils.timezone import now
# Create your models here.


class ProductModel(models.Model):
    sku = models.CharField(max_length=255, primary_key=True, default=None)
    name = models.CharField(max_length=255, default=None)
    description = models.TextField(default=None)
    is_active = models.BooleanField(default=None)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.CASCADE,),
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name


class ProductUploadModel(models.Model):
    name = models.CharField(max_length=255, default=None)
    path = models.FileField(upload_to='csvs/%Y/%m/%d/',
                            verbose_name='Document')
    size = models.IntegerField(default=0)
    imported_rows = models.IntegerField(default=0)
    status = models.CharField(max_length=16, default='Queued')
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.CASCADE,),
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name


class WebhookModel(models.Model):
    name = models.CharField(max_length=255, default=None)
    url = models.URLField(max_length=500, default=None, verbose_name='URL')
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.CASCADE,),
    is_active = models.BooleanField(default=None)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name
