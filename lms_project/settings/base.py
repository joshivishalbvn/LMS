import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR

# <------------------------------ Security ---------------------------------->
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = True
ALLOWED_HOSTS = []
# <------------------------------ Security ---------------------------------->

# <-------------------------------- Apps ------------------------------------>
THIRD_PARTY_APPS = [
    'allauth',
    'allauth.account', 
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'crispy_forms',
    'crispy_bootstrap4',
    'widget_tweaks',
    'django_recaptcha',
    'ckeditor',
    'django_select2',
    'durationwidget',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    "app_modules.users",
    'app_modules.course',
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS
# <-------------------------------- Apps ------------------------------------>

# <----------------------------- Middleware --------------------------------->
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'lms_project.middleware.custom_middlewares.DatabaseQueryLoggingMiddleware',
    'lms_project.middleware.custom_middlewares.DebuggingMiddleware',

]
# <----------------------------- Middleware --------------------------------->

# <--------------------------- URL Configuration ---------------------------->
ROOT_URLCONF = 'lms_project.urls'
# <--------------------------- URL Configuration ---------------------------->

# <------------------------------ Templates --------------------------------->
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR/"templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# <-------------------------------- Templates ------------------------------->

WSGI_APPLICATION = 'lms_project.wsgi.application'

# <--------------------------- Database Configuration ----------------------->
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DATABASE_HOST"),
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "PORT": os.environ.get("DATABASE_PORT"),
    }
}
# <--------------------------- Database Configuration ----------------------->

# <--------------------------- Password Validators -------------------------->
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
# <--------------------------- Password Validators -------------------------->

# <--------------------------- Localization --------------------------------->
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True
# <--------------------------- Localization --------------------------------->

# <----------------------------- Static & Media ----------------------------->
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(APPS_DIR, "static")
STATICFILES_DIRS = [os.path.join(APPS_DIR, "static_files")] 
MEDIA_ROOT = os.path.join(APPS_DIR, "media")
MEDIA_URL = "/media/"
# <------------------------------ Static & Media ----------------------------->

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# <-------------------------- Override Default Data -------------------------->
SITE_ID = 1
AUTH_USER_MODEL = "users.User"
# <-------------------------- Override Default Data -------------------------->

# <-------------------------- Superuser Configuration ------------------------>
SUPER_USER = {
    "ADMIN_EMAIL": os.environ.get("ADMIN_EMAIL"),
    "ADMIN_USERNAME": os.environ.get("ADMIN_USERNAME"),
    "ADMIN_PASSWORD": os.environ.get("ADMIN_PASSWORD"),
}
# <-------------------------- Superuser Configuration ------------------------>

# <------------------------------- All Auth ---------------------------------->
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = "/accounts/login"
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = 'http://127.0.0.1:8000/accounts/google/login/callback/'
SOCIAL_AUTH_GOOGLE_OAUTH2_LOGOUT_URL = 'https://accounts.google.com/Logout'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '',
            'secret': '',
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}
# <------------------------------- All Auth ---------------------------------->

# <-------------------------------- Logging ---------------------------------->
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    
    'formatters': {
        'detailed': {
            'format': '{asctime} {levelname} {name} {funcName} [Line:{lineno}] - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',  
        },
        'simple': {
            'format': '{levelname} - {message}',
            'style': '{',
        },
    },
    
    'handlers': {
        'console': {
            'level': 'DEBUG',  
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
        },
        
    },
}
# <-------------------------------- Logging ---------------------------------->

# <-------------------------------- Crispy ----------------------------------->
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"
# <-------------------------------- Crispy ----------------------------------->

# <-------------------------------- Recaptcha -------------------------------->
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
# <-------------------------------- Recaptcha -------------------------------->

# <------------------------------- CK Editor --------------------------------->
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = "https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js" 
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar_Basic": [["Source", "Bold", "Italic"]],
        "toolbar_YourCustomToolbarConfig": [
            {
                "name": "document",
                "items": [
                    "Source",
                    "Preview",
                ],
            },
            {
                "name": "clipboard",
                "items": [
                    "Cut",
                    "Copy",
                    "Paste",
                    "Undo",
                    "Redo",
                ],
            },
            {"name": "editing", "items": ["Find", "Replace", "SelectAll"]},
            {
                "name": "forms",
                "items": [],
            },
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "Subscript",
                    "Superscript",
                    "RemoveFormat",
                ],
            },
            {"name": "colors", "items": ["TextColor", "BGColor"]},
            {"name": "tools", "items": ["Maximize"]},
            {
                "name": "paragraph",
                "items": [
                    "NumberedList",
                    "BulletedList",
                    "Outdent",
                    "Indent",
                ],
            },
            {"name": "links", "items": ["Link", "Unlink"]},
            {
                "name": "insert",
                "items": [
                    "Table",
                    "HorizontalRule",
                ],
            },
            {
                "name": "styles",
                "items": ["Styles", "Format", "Font", "FontSize"],
            },
        ],
        "toolbar": "YourCustomToolbarConfig",  
        "toolbarGroups": [{"name": "document", "groups": ["mode", "document", "doctools"]}],
        "height": 300,
        "width": "100%",
        "toolbarCanCollapse": False,
        "tabSpaces": 4,
    }
}
# <------------------------------- CK Editor --------------------------------->

# <-------------------------------- Celery ----------------------------------->
CELERY_BROKER_URL = 'redis://localhost:6379/0'  
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
# <-------------------------------- Celery ----------------------------------->


# <-------------------------------- Email ------------------------------------>
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587  
EMAIL_USE_TLS = True 
EMAIL_USE_SSL = False  
EMAIL_HOST_USER = ''  
EMAIL_HOST_PASSWORD = ''  
# <-------------------------------- Email ------------------------------------>


# <-------------------------------- Select 2 ---------------------------------->

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    'select2': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SELECT2_CACHE_BACKEND = 'default'
# <-------------------------------- Select 2 ---------------------------------->