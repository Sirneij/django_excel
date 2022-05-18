web: gunicorn django_excel.wsgi --log-file -
worker: celery -A django_excel worker -l info -B