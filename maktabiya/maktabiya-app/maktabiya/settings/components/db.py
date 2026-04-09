# Database
from maktabiya.settings import env, BASE_DIR

if env("DB_ENGINE") == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": env("DB_NAME", default="maktabiya"),
            "USER": env("DB_USERNAME", default="maktabiya"),
            "PASSWORD": env("DB_PASS", default="maktabiya"),
            "HOST": env("DB_HOST", default="localhost"),
            "PORT": env("DB_PORT", default=3306),
            "CONN_HEALTH_CHECKS": True,
        },
    }
elif env("DB_ENGINE") == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME", default="maktabiya"),
            "USER": env("DB_USERNAME", default="maktabiya"),
            "PASSWORD": env("DB_PASS", default="maktabiya"),
            "HOST": env("DB_HOST", default="localhost"),
            "PORT": env("DB_PORT", default=5432),
            "CONN_MAX_AGE": env.int("DB_CONN_MAX_AGE", default=60),
            # Optional but good practice
            "OPTIONS": {
                "connect_timeout": 60,
            },
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "maktabiya.sqlite3",
        }
    }

# 900 seconds = 15 min
DB_CHECK_SLEEP_DURATION = env("DB_CHECK_SLEEP_DURATION", default=900)
