"""
Django settings for strayballoon project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os

from dotenv import find_dotenv, load_dotenv
from pathlib import Path

load_dotenv(find_dotenv(os.environ.get('ENV_PATH') or '.env.example'))
PYTHON_ENV = os.environ.get('PYTHON_ENV')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_URL = os.environ.get('BASE_URL')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SB_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if PYTHON_ENV != 'production' else False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
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

ROOT_URLCONF = 'strayballoon.urls'

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

WSGI_APPLICATION = 'strayballoon.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL[:7] == 'mongodb':
    DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'NAME': 'strayballoon-dev',
            'CLIENT': {
                'host': DATABASE_URL
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'strayballoon-dev',
            'CLIENT': {
                'host': DATABASE_URL
            }
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-au'

TIME_ZONE = 'Australia/Melbourne'

USE_I18N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

if os.environ.get('PYTHON_ENV') == 'development':
    STATIC_ROOT = BASE_DIR.as_posix() + '/dist'
    STATIC_URL = BASE_URL + 'static/'
else:
    STATIC_ROOT = '/var/www/backend'
    STATIC_URL = BASE_URL + 'static/'

CSRF_TRUSTED_ORIGINS = ['strayballoon.phungnnl.dev']

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Django Rest Framework config
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}
# drf_spectacular settings
SPECTACULAR_SETTINGS = {
    'TITLE': 'StrayBalloon',
    'DESCRIPTION': 'Swinburne Tech Enquiry Project',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}
