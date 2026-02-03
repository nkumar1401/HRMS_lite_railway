web: gunicorn HRMS_lite.wsgi --log-file -
web: python manage.py migrate && gunicorn HRMS_lite.wsgi --log-file -