web: gunicorn brazen.conf.wsgi --capture-output --log-level info --workers 2
worker: python manage.py run_huey
release: python manage.py migrate