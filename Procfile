release: python manage.py migrate --settings=settings.production
web: gunicorn loadify.asgi -k uvicorn.workers.UvicornWorker --log-file -
worker: celery worker -A loadify