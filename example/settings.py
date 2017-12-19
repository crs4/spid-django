"""
Django settings for spiddjango project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!td4zwz+%kchoz)q_je6ep&vg!u&22^1ey5we$ks2n&megh3c='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['spid.testsp.it']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangosaml2',
    'spiddjango',
    'sslserver'
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'djangosaml2.backends.Saml2Backend',
]

ROOT_URLCONF = 'example.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'example.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
LOGIN_URL = '/saml2/login/'

HOSTNAME = 'spid.testsp.it'
ROOT_URL = 'https://' + HOSTNAME + ':9000'

SAML_SP_NAME = 'Examples Service Provider'
SAML_SP_KEY_PATH = os.path.join(os.path.dirname(__file__), './certs/key.pem')
SAML_SP_CRT_PATH = os.path.join(os.path.dirname(__file__), './certs/cert.pem')
from spiddjango.utils import get_saml_config
SAML_CONFIG = get_saml_config(ROOT_URL, SAML_SP_NAME, SAML_SP_KEY_PATH, SAML_SP_CRT_PATH)
SAML_AUTHN_CUSTOM_ARGS = {
    'attribute_consuming_service_index': '1'
}
SAML_ATTRIBUTE_MAPPING = {
    'spidCode': ('username',),
    'fiscalNumber': ('fiscalNumber',),
    "name": ('first_name',),
    # "gender": ('gender',),
    # "ivaCode": ('iva_code',),
    # "placeOfBirth": ('place_of_birth',),
    # "companyName": ('company_name',),
    # "mobilePhone": ('mobile_phone',),
    # "expirationDate": ('expiration_date',),
    # "address": ('address',),
    # "digitalAddress": ('digital_address',),
    "email": ('email',),
    # "registeredOffice": ('registered_office',),
    # "idCard": ('username',),
    # "dateOfBirth": ('date_of_birth',),
    # "countyOfBirth": ('county_of_birth',),
    "familyName": ('last_name',),
}
AUTH_USER_MODEL = 'spiddjango.SpidUser'
