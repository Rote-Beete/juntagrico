from .base import *  # noqa: F401, F403

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-b6yfyftr*!fl6g6!c8k&6!2arf-s=2!b*0=s5%nq15vb8dss*m"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

for key in os.environ.keys():
    if key.startswith("JUNTAGRICO_EMAIL_WHITELISTED"):
        whitelist_email_from_env(key)

CRISPY_FAIL_SILENTLY = False
