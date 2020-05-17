"""
Celery Tasks to handle pulling data from host and run the task in background without overloading server.
"""

# from __future__ import absolute_import, unicode_literals
from .models import ProductModel, ProductUploadModel
import logging
import csv
import os
import random
import requests

from datetime import datetime
from django.utils import timezone

from celery import shared_task
from django.conf import settings
from django_pg_bulk_update import bulk_update_or_create


def update_job_status(job_id, status, count):
    ProductUploadModel.objects.filter(id=job_id).update(
        status=status, updated_at=datetime.now(tz=timezone.utc), imported_rows=count)
    base_url = os.environ['DJANGO_SERVER_URL']
    requests.get(base_url + 'products/uploads/events',
                 params={'id': job_id, 'status': status, 'count': count})


@shared_task
def import_csv(import_job_id, file_path):
    count = 0

    update_job_status(import_job_id, 'Processing', count)

    try:
        file_object = open('%s%s' % (settings.MEDIA_ROOT, file_path))
        reader = csv.DictReader(file_object)
        rows = []
        for row in reader:
            row['sku_orig'] = row['sku']
            row['sku'] = row['sku'].lower()
            row['is_active'] = random.choice([True, False])
            rows.append(row)
            count += 1
            if count % 100 == 0:
                res = bulk_update_or_create(
                    ProductModel, rows, key_fields='sku')
                update_job_status(import_job_id, 'Processing', count)
                rows = []
                logging.info('Imported %d rows' % count)

        if rows:
            res = bulk_update_or_create(ProductModel, rows, key_fields='sku')

        logging.info('Import finished with %d rows' % count)

        update_job_status(import_job_id, 'Completed', count)
    except Exception as e:
        logging.error(e)
        update_job_status(import_job_id, 'Failed', count)
