import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv
from bnb.env import Environment

ORGANISATION_WEBSITE = "rotebeete.org"
ADMINPORTAL_NAME = "juntagrico.rotebeete.org"
ADMINPORTAL_SERVER_URL = "juntagrico.rotebeete.org"

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR / ".env.local")
env = Environment("ROTEBEETE_")


DATA_DIR = env.get("DATA_DIR", cast=Path, default=BASE_DIR / "data")
DATA_DIR.mkdir(exist_ok=True)

SECRET_KEY = env.get("SECRET_KEY", default="") or None

DEBUG = env.is_true("DEBUG", default=False)

ALLOWED_HOSTS = env.get_list("ALLOWED_HOSTS", default=["localhost"])


IMPERSONATE = {
    "REDIRECT_URL": "/my/profile",
}

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "impersonate",
    "rotebeete",
    "juntagrico",
    "crispy_forms",
    "adminsortable2",
    "djrichtextfield",
    "defender",
    "polymorphic",
    "oauth2_provider",
    "rotebeete.transitions",
    'import_export',
    'biddings',
    # enable only to test addon stuff
    # 'juntagrico_test_addon',
]


ROOT_URLCONF = "rotebeete.urls"

AUTHENTICATION_BACKENDS = (
    "juntagrico.util.auth.AuthenticateWithEmail",
    "django.contrib.auth.backends.ModelBackend",
)

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "impersonate.middleware.ImpersonateMiddleware",
    "rotebeete.transitions.middleware.ReviewMiddleware",
]

DEFAULT_FROM_EMAIL = "no-reply@rotebeete.org"

STATIC_ROOT = DATA_DIR / "public" / "static"
STATIC_URL = "/static/"

LANGUAGE_CODE = "de-DE"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

DATE_INPUT_FORMATS = [
    "%d.%m.%Y",
]

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

TIME_ZONE = "Europe/Berlin"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["/data/juntagrico/rotebeete/templates/"],
        "OPTIONS": {
            "context_processors": [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "debug": False,
        },
    },
]


DATABASES = {
    "default": dj_database_url.parse(
        env.get("DATABASE_URL", default=f"sqlite:///{DATA_DIR / 'db.sqlite'}"),
    )
}

LOGIN_REDIRECT_URL = "/my/home"

SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

LOCALE_PATHS = (BASE_DIR / "juntagrico/locale",)

CRISPY_TEMPLATE_PACK = "bootstrap4"
CRISPY_FAIL_SILENTLY = env.is_true("CRISPY_FAIL_SILENTLY", default=True)

DJRICHTEXTFIELD_CONFIG = {
    "js": ["/static/juntagrico/external/tinymce/tinymce.min.js"],
    "init_template": "djrichtextfield/init/tinymce.js",
    "settings": {
        "menubar": False,
        "plugins": "link  lists",
        "toolbar": "undo redo | bold italic | alignleft aligncenter alignright alignjustify | outdent indent | bullist numlist | link",
    },
}

WSGI_APPLICATION = "rotebeete.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Juntagrico settings
# https://github.com/juntagrico/juntagrico/blob/main/juntagrico/config.py

ENABLE_REGISTRATION = False

SHARE_PRICE = 50


# this might be used to temporarily disable email sending
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFENDER_BEHIND_REVERSE_PROXY = True
DEFENDER_LOCKOUT_URL = "https://rotebeete.org/organisation/kontakt/"
DEFENDER_REDIS_URL = "redis://127.0.0.1:6379/0"


ORGANISATION_NAME = "SoLaWi Rote Beete"
ORGANISATION_LONG_NAME = (
    "Gemüsekooperative Rote Beete eG (Adresse etc. https://rotebeete.org/impressum/)"
)
ORGANISATION_ADDRESS = {
    "name": "Gemüsekooperative Rote Beete eG",
    "street": "An der Schmiede",
    "number": "4",
    "zip": "04425",
    "city": "Sehlis/Taucha",
    "extra": "",
}
ORGANISATION_PHONE = "034298-495168"
BUSINESS_YEAR_START = {"day": 1, "month": 7}
BUSINESS_YEAR_CANCELATION_MONTH = 3
CONTACTS = {"info": "invalid@rotebeete.invalid"}
VOCABULARY = {
    "member": "Mitglied",
    "member_pl": "Mitglieder",
    "assignment": "Arbeitseinsatz",
    "assignment_pl": "Arbeitseinsätze",
    "share": "Genossenschaftsanteil",
    "share_pl": "Genossenschaftsanteile",
    "subscription": "Gemüseanteil",
    "subscription_pl": "Gemüseanteile",
    "co_member": "Mitessende",
    "co_member_pl": "Mitessende",
    "price": "Beitrag",
    "member_type": "Mitglied",
    "member_type_pl": "Mitglieder",
    "depot": "Verteilstation",
    "depot_pl": "Verteilstationen",
    "package": "Kiste",
}

STYLES = {"static": ["rotebeete/css/rotebeete.css", "biddings/css/biddings.css"]}

WHITELIST_EMAILS = []


def whitelist_email_from_env(var_env_name):
    email = os.environ.get(var_env_name)
    if email:
        WHITELIST_EMAILS.append(email)


for key in os.environ.keys():
    if key.startswith("JUNTAGRICO_EMAIL_WHITELISTED"):
        whitelist_email_from_env(key)
