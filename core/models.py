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
    path = models.CharField(max_length=500, default=None)
    total_rows = models.IntegerField(default=0)
    processed_rows = models.IntegerField(default=0)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.CASCADE,),
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name


class WebhookModel(models.Model):
    name = models.CharField(max_length=255, default=None)
    path = models.CharField(max_length=500, default=None)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.CASCADE,),
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name
