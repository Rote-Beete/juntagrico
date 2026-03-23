import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env()

env.prefix = "ROTEBEETE_"

environ.Env.read_env(BASE_DIR / ".env")
environ.Env.read_env(BASE_DIR / ".env.local")

DATA_DIR = env("DATA_DIR", cast=Path, default=BASE_DIR / "data")
DATA_DIR.mkdir(exist_ok=True)

ALLOWED_HOSTS = env("ALLOWED_HOSTS", cast=list, default=[])
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS", cast=list, default=[])
DEBUG = env("DEBUG", cast=bool, default=False)
ORGANISATION_WEBSITE = {"name": "rotebeete.org", "url": "https://rotebeete.org"}

SECRET_KEY = env("SECRET_KEY", cast=str)


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
    "rotebeete",
    "rotebeete.transitions",
    "juntagrico",
    "fontawesomefree",
    "import_export",
    "impersonate",
    "crispy_forms",
    "adminsortable2",
    "djrichtextfield",
    "defender",
    "oauth2_provider",
    "polymorphic",
    "biddings",
]

DATABASES = {
    "default": env.db("DATABASE_URL", default=f"sqlite:///{DATA_DIR / 'db.sqlite3'}")
}

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
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "defender.middleware.FailedLoginMiddleware",
]

EMAIL_HOST = "mail.rotebeete.org"
EMAIL_HOST_USER = "invalid@rotebeete.invalid"
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", cast=str)
EMAIL_PORT = "587"
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = "invalid@rotebeete.invalid"

WHITELIST_EMAILS = []


def whitelist_email_from_env(var_env_name):
    email = os.environ.get(var_env_name)
    if email:
        WHITELIST_EMAILS.append(email)


for key in os.environ.keys():
    if key.startswith("JUNTAGRICO_EMAIL_WHITELISTED"):
        whitelist_email_from_env(key)

STATIC_ROOT = DATA_DIR / "public" / "static"
STATIC_URL = "/static/"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

IMPORT_EXPORT_EXPORT_PERMISSION_CODE = "view"

LANGUAGE_CODE = env("LANGUAGE_CODE", cast=str, default="de-DE")

TIME_ZONE = env("TIME_ZONE", cast=str, default="Europe/Berlin")

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


STYLES = {"static": ["rotebeete/css/rotebeete.css", "biddings/css/biddings.css"]}

SCRIPTS = {"static": ["biddings/js/biddings.js"]}


class InvalidTemplateVariable(str):
    def __mod__(self, other):
        raise NameError(
            f"In template, undefined variable or unknown value for: '{other}'"
        )


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
                "juntagrico.context_processors.vocabulary",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            # 'string_if_invalid': InvalidTemplateVariable("%s"),
            "debug": False,
        },
    },
]


LOGIN_REDIRECT_URL = "/my/home"

SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"

LOCALE_PATHS = (BASE_DIR / "juntagrico/locale",)

CRISPY_TEMPLATE_PACK = "bootstrap4"
CRISPY_FAIL_SILENTLY = env("CRISPY_FAIL_SILENTLY", cast=bool, default=True)

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
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

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
CONTACTS = {"general": "invalid@rotebeete.invalid"}
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
CURRENCY = "EUR"

ORGANISATION_BANK_CONNECTION = {
    "IBAN": "-",
    "BIC": "-",
    "NAME": "-",
}

# DEFENDER: Brute Force Protection
##################################

DEFENDER_BEHIND_REVERSE_PROXY = True
DEFENDER_LOCKOUT_URL = "https://rotebeete.org/organisation/kontakt/"

DEFENDER_REDIS_URL = env("DEFENDER_REDIS_URL", default="redis://127.0.0.1:6379/0")
# OIDC/ OAuth2 fuer Wikijs
##########################
# https://django-oauth-toolkit.readthedocs.io/en/latest/oidc.html
# Schluessel per ENV einlesen - ist in /etc/uwsgi/apps-enabled/rotebeete.ini definiert
# Klasse definieren, um weitere claims/Daten ans Wiki zu senden

# https://django-oauth-toolkit.readthedocs.io/en/latest/changelog.html#id5
# WikiJS unterstuetzt kein PKCE
# https://github.com/requarks/wiki/discussions/6384

try:
    oidc_key_filename = os.getenv("OIDC_RSA_PRIVATE_KEY_FILE")
    with open(oidc_key_filename, "r") as key_file:
        oidc_key = key_file.read()

    OAUTH2_PROVIDER = {
        "OIDC_ENABLED": True,
        "PKCE_REQUIRED": False,
        "OIDC_RSA_PRIVATE_KEY": oidc_key,
        "OAUTH2_VALIDATOR_CLASS": "rotebeete.oauth_validators.AccountOAuth2Validator",
        "SCOPES": {
            "openid": "OpenID Connect scope",
            "email": "Email scope",
            "profile": "Profile scope",
        },
    }
except (NameError, TypeError):
    pass
