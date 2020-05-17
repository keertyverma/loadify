release: python manage.py migrate --settings=settings.production
web: daphne loadify.asgi:application --port $PORT --bind 0.0.0.0
worker: celery worker -A loadify