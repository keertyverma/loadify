from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.db import connection
# Create your models here.


class ProductModel(models.Model):
    sku = models.CharField(max_length=255, primary_key=True, default=None)
    sku_orig = models.CharField(
        max_length=255, default=None, verbose_name='SKU')
    name = models.CharField(max_length=255, default=None)
    description = models.TextField(default=None)
    is_active = models.BooleanField(default=None)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                          on_delete=models.CASCADE,),
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute(
                'TRUNCATE TABLE {} CASCADE'.format(cls._meta.db_table))


class ProductTruncateModel(models.Model):
    created_at = models.DateTimeField(default=now, editable=False)


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

    class Meta:
        ordering = ['-created_at']


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
