from maktabiya.settings import env

if env("SESSION_CACHE_BACKEND", default="") == "memcache":
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
            # TIMEOUT is not the connection timeout! It's the default expiration
            # timeout that should be applied to keys! Setting it to `None` disables expiration.
            "TIMEOUT": 3600,
            "LOCATION": env(
                "SESSION_STORAGE_SERVER", default="maktabiya-memcached:11211"
            ),
        }
    }
else:
    # FileBasedCache is better for Dev
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": "/tmp/django_cache",
        }
    }
