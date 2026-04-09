from pathlib import Path
from split_settings.tools import include, optional
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
base_settings = (
    # can be used also components/*.py but i prefer to explicit
    "components/app_*.py",
    "components/caches.py",
    "components/common.py",
    "components/cron_*.py",
    "components/db.py",
    "components/email_*.py",
    "components/log.py",
    # Optionally override some settings:
    optional("components/local.py"),
)

# Include settings:
include(*base_settings)
