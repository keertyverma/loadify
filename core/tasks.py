"""
Celery Tasks to handle pulling data from host and run the task in background without overloading server.
"""

# from __future__ import absolute_import, unicode_literals
import logging
import csv
import os
import random

from datetime import datetime
from django.utils import timezone

from celery import shared_task
from django.conf import settings
from django_pg_bulk_update import bulk_update_or_create, pdnf_clause

from .models import ProductModel, ProductUploadModel


@shared_task
def import_csv(import_job_id, file_path):
    count = 0

    try:
        file_object = open('%s%s' % (settings.MEDIA_ROOT, file_path))
        reader = csv.DictReader(file_object)
        rows = []
        for row in reader:
            row['sku_orig'] = row['sku']
            row['sku'] = row['sku'].lower()
            row['is_active'] = random.choice([True, False])
            logging.info(row)
            rows.append(row)
            count += 1
            if count % 100 == 0:
                res = bulk_update_or_create(
                    ProductModel, rows, key_fields='sku')
                rows = []
                logging.info('Imported %d rows' % count)

        if rows:
            res = bulk_update_or_create(ProductModel, rows, key_fields='sku')

        logging.info('Import finished with %d rows' % count)

        ProductUploadModel.objects.filter(id=import_job_id).update(
            status='Completed', updated_at=datetime.now(tz=timezone.utc), imported_rows=count)
    except Exception as e:
        logging.error(e)
        ProductUploadModel.objects.filter(id=import_job_id).update(
            status='Failed', updated_at=datetime.now(tz=timezone.utc), imported_rows=count)
