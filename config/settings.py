import os

import environ

from pathlib import Path

env = environ.Env(DEBUG=(bool, False))

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env.str('DJANGO_SECRET_KEY', 'default-secret-key')

DEBUG = env.bool('DJANGO_DEBUG', False)

ALLOWED_HOSTS = ['*']

DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

DJANGO_APPS = [
    'src.api.apps.ApiConfig',
    'src.teasers.apps.TeasersConfig',
    'src.users.apps.UsersConfig',
    'src.wallets.apps.WalletsConfig',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'drf_yasg',
    'query_counter',
]

INSTALLED_APPS = DEFAULT_APPS + DJANGO_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'query_counter.middleware.DjangoQueryCounterMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('POSTGRES_HOST'),
        'PORT': env.str('POSTGRES_PORT'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'description': 'Вход по токену. Формат ввода: Token <ВАШ ТОКЕН>',
            'in': 'header',
        }
    },
    'USE_SESSION_AUTH': False,
    'DEFAULT_AUTO_SCHEMA_CLASS': 'src.api.swagger.schemas.CustomAutoSchema',
}

DJOSER = {
    'LOGIN_FIELD': 'username',
    'HIDE_USERS': False,
    'SEND_ACTIVATION_EMAIL': False,
    'SERIALIZERS': {
        'user': 'src.api.serializers.users.UserSerializer',
        'current_user': 'src.api.serializers.users.CurrentUserSerializer',
    },
}

LOGS_DIR = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)

LOG_LEVEL = env.str('DJANGO_LOG_LEVEL', default='DEBUG')
LOGGER_LINE_SEPARATOR = "-" * 80
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file': {
            'format': f'{LOGGER_LINE_SEPARATOR}\n'
            '{asctime} - {name} - {levelname}'
            ' - {module} - {filename} - {message}',
            'style': '{',
        }
    },
    'handlers': {
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'logger.log'),
            'formatter': 'file',
            'encoding': 'UTF-8',
        }
    },
    'loggers': {
        'django.request': {
            'level': LOG_LEVEL,
            'handlers': ['file'],
            'propagate': True,
        },
        'django.db.backends': {
            'level': LOG_LEVEL,
            'handlers': ['file'],
            'propagate': True,
        },
    },
}
