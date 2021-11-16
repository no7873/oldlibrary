"""
Django settings for config project.
Generated by 'django-admin startproject' using Django 3.1.5.
For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import pymysql
import dj_database_url

pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'accounts.apps.AccountsConfig',
    'shop',
    'django.contrib.sites',
    'cart',
    'rcart',
    'order',
    'rental',
    'search',
    'home',
    'rentorder',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
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


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'heroku_fb1e6c2edf9278e',
        'USER' : 'b8a8bdf0b497f0',
        'PASSWORD' : 'f9125a3e',
        'HOST' : 'us-cdbr-east-04.cleardb.com',
        'PORT' : '3306',
    }
}

DATABASES['default'].update(dj_database_url.config(conn_max_age=500))

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ko'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# STATIC_URL = '/static/'
AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = 'oldlibrary-gsg'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
AWS_S3_FILE_OVERWRITE = False # 같은 이름 파일이 있는 경우 덮어 쓸지 설정
# 파일 받아갔을 때 cache를 얼마나 유지할 것인지 설정
AWS_S3_OBJECT_PARAMETERS = {
'CacheControl': 'max-age=86400',
}
AWS_DEFAULT_ACL = 'public-read' # 이렇게 설정하지 않으면 외부 접근이 안되서 못보는 경우가 생
AWS_LOCATION = 'static'

STATIC_URL = 'http://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FILE_STORAGE = 'config.asset_storage.MediaStorage'

STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT=BASE_DIR/ 'static_files'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CART_ID = 'cart_in_session'
SITE_ID = 1

IAMPORT_KEY = '9365271867084088'
IAMPORT_SECRET = '2Dk7mTHlgoTv61oKMqEdsv2tKLb6ckGeY1mlU4GbsAGyB4jouXBXtDrdoCjBX0QV2chWhX7JxOi9SBxn'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTH_USER_MODEL='accounts.User'

# SECURITY WARNING: keep the secret key used in production secret!

import os, json
from django.core.exceptions import ImproperlyConfigured

if os.path.isfile(os.path.join(BASE_DIR, 'secrets.json')) == True:
    secret_file = os.path.join(BASE_DIR, 'secrets.json')

    with open(secret_file) as f:
        secrets = json.loads(f.read())

    def get_secret(setting, secrets=secrets):
        """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
        try:
            return secrets[setting]
        except KeyError:
            error_msg = "Set the {} environment variable".format(setting)
            raise ImproperlyConfigured(error_msg)

    SECRET_KEY = get_secret("SECRET_KEY")

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER = get_secret("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

    AWS_ACCESS_KEY_ID = get_secret("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = get_secret("AWS_SECRET_ACCESS_KEY")
else:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER =  os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD =  os.environ.get("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")