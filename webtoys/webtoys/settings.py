"""
Django settings for webtoys project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from webtoys.options import get_boolean,get_string,get_float
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PRODUCT_DIR = os.path.join('/opt', 'webtoys', 'current')

VAR_DIR = '/var/webtoys'

# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_string( 'django','secret_key')
assert SECRET_KEY, """You didn't set up a /etc/webtoys/secretkey.conf with [django]\nsecret_key=..."""

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_boolean( 'django','debug', False )
TEMPLATE_DEBUG = DEBUG
ASSETS_DEBUG = DEBUG

EMAIL_HOST = 'mail.vex.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mcfletc2'
EMAIL_HOST_PASSWORD = get_string('email','password', None)
EMAIL_USE_TLS = True
assert EMAIL_HOST_PASSWORD,  "You didn't specify an [email]\npassword=... key in the /etc/webtoys/*.conf"

ALLOWED_HOSTS = [
    get_string( 'django','allowed_hosts','webtoys.vrplumber.com'),
]

INSTALLED_APPS = (
    'toys',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'django_nose',
    'django_assets',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
)

ROOT_URLCONF = 'webtoys.urls'

WSGI_APPLICATION = 'webtoys.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'webtoys',
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False 

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join( PRODUCT_DIR, 'www', 'static')

if DEBUG:
    TEMPLATE_LOADERS = [
        'django.template.loaders.app_directories.Loader',
    ]
else:
    TEMPLATE_LOADERS = [
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.app_directories.Loader',
        )),
    ]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',    
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(VAR_DIR,'django-cache'),
    }, 
    'utterances': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(VAR_DIR,'utterances-cache'),
    }, 
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile': {
            'level': 'WARN',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(VAR_DIR, 'log', 'django.log'),
            'maxBytes': 1024*1024,
            'backupCount': 2,
            'formatter': 'standard',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        '': {
            'level': 'DEBUG',
            'handlers': ['logfile'],
        },
    }
}
