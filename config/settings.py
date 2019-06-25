"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import secret_key

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # debug toolbar
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+$#!u3%%c=@dai(q2a%-o517pxf--f7bpb22=@*#gmxz=i-8oe'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # deploy mode - False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'photo',
    'disqus',
    'django.contrib.sites',
    'storages',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.naver',
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
        'DIRS': [os.path.join(BASE_DIR, 'layout')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },

]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
#

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

import dj_database_url

DATABASES['default'].update(dj_database_url.config(conn_max_age=500))

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ko-KR'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# static과 media를 S3를 올려야한다
# boto3 : amazonS3를 사용할 수 있도록 함
# pip install boto3
# django-storages : 장고 프로젝트에서 특정 storage를 사용할 수 있도록 함
# pip install django-storages
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
#
AWS_ACCESS_KEY_ID = secret_key.key['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = secret_key.key['AWS_SECRET_ACCESS_KEY']
AWS_REGION = 'ap-northeast-2'
AWS_STORAGE_BUCKET_NAME = secret_key.key['AWS_STORAGE_BUCKET_NAME']  # static
AWS_S3_CUSTOM_DOMAIN = 's3.%s.amazonaws.com/%s' % (AWS_REGION, AWS_STORAGE_BUCKET_NAME)
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_S3_SECURE_URLS = True
AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'static'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # local
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # heroku
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)  # s3
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'  # s3
DEFAULT_FILE_STORAGE = 'config.asset_storage.MediaStorage'

LOGIN_REDIRECT_URL = '/'
# login 이후 '/'로 이동
from django.urls import reverse_lazy

LOGIN_URL = reverse_lazy('accounts:signin')

# django-disqus : db가 필요없다 -> disqus.com에서 관리(model, migration이 필요없다)
# django.contrib.sites : 프로젝트 사이트 정보 관리 -> db가 필요하기 때문에 Migration 필요
DISQUS_WEBSITE_SHORTNAME = 'wpsdstagram-1493'

SITE_ID = 1
