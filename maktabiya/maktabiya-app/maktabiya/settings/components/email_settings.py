from maktabiya.settings import env

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="maktabiya-mail-server")
EMAIL_TIMEOUT = env(
    "EMAIL_TIMEOUT", default=60
)  # Set the desired timeout value in second
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@AladinStudioX.app")
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL  # don't edit this!
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_PORT = env("EMAIL_PORT", default=25)
EMAIL_USE_TLS = env("EMAIL_USE_TLS", default=False)
