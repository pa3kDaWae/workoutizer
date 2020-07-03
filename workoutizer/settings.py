import os
import configparser

import coloredlogs


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
TRACKS_DIR = os.path.join(BASE_DIR, 'tracks')
CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')
INITIAL_TRACE_DATA_DIR = os.path.join(BASE_DIR, 'setup', 'initial_trace_data')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


# read config values
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h#ppx^(%ya18qrm+hgzf-vxr^t=r57k_65_hr73f^-n)@qc9as'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'wizer',
    'leaflet',
    'colorfield',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'workoutizer.urls'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

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

WSGI_APPLICATION = 'workoutizer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
sqlite_file = 'db.sqlite3'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, sqlite_file),
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_L10N = True
USE_TZ = True

PLOT_WIDTH = 1110
PLOT_HEIGHT = 300

format_console = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
# format_console = "%(name)s - %(message)s"  # optionally add time: "%(asctime)s -"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'colored': {'()': 'coloredlogs.ColoredFormatter', 'format': format_console, 'datefmt': '%m-%d %H:%M:%S'}
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', config.get('DJANGO', "django_log_level")),
        },
        'wizer': {
            'handlers': ['console'],
            'level': os.getenv('WKZ_LOG_LEVEL', config.get('WORKOUTIZER', 'wkz_log_level')),
        },
    },
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}
