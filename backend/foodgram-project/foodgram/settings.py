import os
from pathlib import Path

DEBUG = True


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "ST_SECRET_KEY",
    default="p&l%385148kslhtyn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs",
)


ALLOWED_HOSTS = ["food_web", "localhost", "foodgram.zapto.org"]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://foodgram.zapto.org",
    "https://foodgram.zapto.org"
]


INSTALLED_APPS = [
    "users.apps.UsersConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "django_filters",
    "api",
    "ingredients",
    "recipes",
    "colorfield",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "foodgram.urls"


TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "foodgram.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": os.getenv(
            "DB_ENGINE",
            default="django.db.backends.postgresql",
        ),
        "NAME": os.getenv("DB_NAME", default="foodgram"),
        "USER": os.getenv("DB_USER", default="foodgram"),
        "PASSWORD": os.getenv("DB_PASSWORD", default="foodgram"),
        "HOST": os.getenv("DB_HOST", default="localhost"),
        "PORT": os.getenv("DB_PORT", default="5432"),
    }
}

AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation."
        "NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_PAGINATION_CLASS": "api.pagination.CustomPagination",
    "PAGE_SIZE": 5,
}


DJOSER = {
    "LOGIN_FIELD": "email",
}

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Istanbul"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

PDF_PAGE_SIZE = "A4"

MESSAGES = {
    "username_invalid": "This username is not allowed to be used",
    "current_password_invalid": "Invalid current password.",
    "greater_zero": "Value must be greater than zero",
    "self_subscription": "Self-subscription is not allowed.",
    "double_subscription": "Double Subscription is not allowed.",
    "no_subscribed": "Unsubscribe error, you were not subscribed",
    "relation_already_exists": "This relation is already exists.",
    "relation_not_exists": "Cannot delete. This relation doesn't exist.",
    "patch_only_author": "Update recipe can only author or admin.",
    "ingredients_requared": "Recipe ingredients required.",
    "ingredients_unic": "Ingredients for recipe must be unique.",
    "tags_requared": "Recipe tags required.",
    "pdf_about": "Enjoy your meal! (c)Foodogram by web2cap github.com/web2cap",
}
