# -*- encoding: utf-8 -*-

import os

wsgi_app = "maktabiya.wsgi:application"
bind = "0.0.0.0:8000"
reload = os.getenv("DEBUG", False)
loglevel = os.getenv("DJANGO_APP_LOG_LEVEL", "error").lower()
workers = 4
threads = 4
worker_class = "gthread"
accesslog = "-"
errorlog = "-"
timeout = os.getenv("GUNICORN_TIMEOUT", 120)
graceful_timeout = os.getenv("GUNICORN_TIMEOUT", 120)
keepalive = os.getenv("GUNICORN_TIMEOUT", 120)
capture_output = True
enable_stdio_inheritance = True
# Not Every OS might be supported, remove if necessary!
worker_tmp_dir = "/dev/shm"

# ssl key file
keyfile = os.getenv("GUNICORN_KEYFILE", None)
# ssl cert file
certfile = os.getenv("GUNICORN_CERTFILE", None)
