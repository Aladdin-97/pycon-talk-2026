from maktabiya.settings import env, BASE_DIR

SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = [env("ALLOWED_HOSTS", default="*")]
# Application definition:
INSTALLED_APPS = [
    # this must be before contrib.admin
    # custom admin interface
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # additional modules
    "rangefilter",
    "widget_tweaks",
    "django_htmx",
    # django management utils modules
    "django_extensions",
    # django background cronjob tasks
    "django_q",
    # maktabiya app modules
    "app_core",
    "booking",
    "email_templates",
    "user",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR.joinpath("templates"),
            BASE_DIR.joinpath("user", "templates", "user"),
            BASE_DIR.joinpath("app_core", "templates", "app_core"),
            BASE_DIR.joinpath("booking", "templates", "booking"),
            BASE_DIR.joinpath("email_templates", "templates", "email_templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Custom app context processor
                "app_core.context_processors.app_metadata",
            ],
            "string_if_invalid": "{{%s}}",
        },
    },
]

# Django authentication system
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # This must be first, if you have multiple auth backend!
)

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


ROOT_URLCONF = "maktabiya.urls"
WSGI_APPLICATION = "maktabiya.wsgi.application"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", default=False)
if DEBUG:
    DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000  # to avoid "Too many fields" error when submitting large forms, adjust as needed
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    TEMPLATES[0]["OPTIONS"]["context_processors"].append(
        "django.template.context_processors.debug"
    )
    # for debugging ip
    INTERNAL_IPS = [env("INTERNAL_IPS", default="localhost")]

# Internationalization
LANGUAGE_CODE = env("LANGUAGE_CODE", default="en-us")
TIME_ZONE = env("TIME_ZONE", default="UTC")
USE_TZ = env("USE_TZ", default=True)
USE_I18N = True


# Static files (CSS, JavaScript, Images)
STATIC_ROOT_DIR = "static_root_dir"

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR.joinpath(STATIC_ROOT_DIR, "staticfiles")

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR.joinpath(STATIC_ROOT_DIR, "mediafiles")

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "user.User"

SESSION_COOKIE_AGE = 3600  # in seconds (1 hour)
SESSION_SAVE_EVERY_REQUEST = env("DEBUG")

# Security

CSRF_TRUSTED_ORIGINS = [
    "http://" + env("APP_DOMAIN", default="localhost"),
    "https://" + env("APP_DOMAIN", default="localhost"),
]
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
