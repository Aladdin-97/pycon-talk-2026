# Disable Django's logging setup
import logging.config
from django.utils.log import DEFAULT_LOGGING

from maktabiya.settings import env

APP_LOGGER = "maktabiya"
LOGGING_CONFIG = None
LOGLEVEL = env("LOGLEVEL", default="DEBUG").upper()
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT = (
    "%(asctime)s - %(name)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s"
    if LOGLEVEL == "DEBUG"
    else "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
)
if env("DEBUG"):
    USER_APP_LOG_LEVEL = "DEBUG"
    DJANGO_APP_LOG_LEVEL = "DEBUG"
else:
    USER_APP_LOG_LEVEL = env("USER_APP_LOG_LEVEL", default=LOGLEVEL)
    DJANGO_APP_LOG_LEVEL = env("DJANGO_APP_LOG_LEVEL", default=LOGLEVEL)

# TODO: Add session id after user log in
logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {"format": LOG_FORMAT, "datefmt": DATE_FORMAT},
            "json": {
                "format": LOG_FORMAT,
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            },
            "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
        },
        "handlers": {
            # console logs to stderr
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "console_json": {"class": "logging.StreamHandler", "formatter": "json"},
            "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
        },
        "loggers": {
            # default for all undefined Python modules
            "": {
                "level": LOGLEVEL,
                "handlers": ["console"],
            },
            # Our application code
            APP_LOGGER: {
                "level": USER_APP_LOG_LEVEL,
                "handlers": ["console"],
                # Avoid double logging because of root logger
                "propagate": False,
            },
            # Django-q
            "django-q": {
                "level": USER_APP_LOG_LEVEL,
                "handlers": ["console"],
                # Avoid double logging because of root logger
                "propagate": False,
            },
            "jazzmin": {
                "level": USER_APP_LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
            # Django logging level
            "django": {
                "level": DJANGO_APP_LOG_LEVEL,
                "handlers": ["console"],
                "propagate": False,
            },
            "gunicorn": {
                "handlers": ["console"],
                "level": DJANGO_APP_LOG_LEVEL,
                "propagate": False,
            },
            # Prevent modules from logging in debug
            "django.template": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": False,
            },
            "environ": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": False,
            },
            "noisy_module": {
                "level": "ERROR",
                "handlers": ["console"],
                "propagate": False,
            },
            # Default runserver request logging
            "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
        },
    }
)
