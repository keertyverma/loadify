# Generated by Django 3.0.6 on 2020-05-17 12:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('sku', models.CharField(default=None, max_length=255, primary_key=True, serialize=False)),
                ('sku_orig', models.CharField(default=None, max_length=255, verbose_name='SKU')),
                ('name', models.CharField(default=None, max_length=255)),
                ('description', models.TextField(default=None)),
                ('is_active', models.BooleanField(default=None)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ProductUploadModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=255)),
                ('path', models.FileField(upload_to='csvs/%Y/%m/%d/', verbose_name='Document')),
                ('size', models.IntegerField(default=0)),
                ('imported_rows', models.IntegerField(default=0)),
                ('status', models.CharField(default='Queued', max_length=16)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='WebhookModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=255)),
                ('url', models.URLField(default=None, max_length=500, verbose_name='URL')),
                ('is_active', models.BooleanField(default=None)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
