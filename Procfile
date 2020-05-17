release: python manage.py migrate --settings=settings.production
web: uvicorn loadify.asgi:application --lifespan on --host=0.0.0.0 --port=${PORT:-5000}
worker: celery worker -A loadify