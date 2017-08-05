"""
Default Django settings fo

Generated by 'django-admin startproject' using Django 1.10.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import dj_database_url

# This line imports a large number of defaults, so that
# they do not need to be specified here directly.
# You may always override these defaults below.
from danceschool.default_settings import *

# This line is required by Django CMS to determine default URLs
# for pages.
SITE_ID = 1

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yw8^8a-lvpa4^#m*2(x)k)t7^th^$fae@=3-b%vuacvh(p!ju*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: ALLOWED_HOSTS must be updated for production
# to permit public access of the site.
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'testserver']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    # Django-allauth is used for better authentication options
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Django-polymorphic is used for Event multi-table inheritance
    'polymorphic',
    # Django-admin-sortable permits us to drag and drop sort page content items
    'adminsortable2',
    # Autocomplete overrides some admin features so it goes here (above admin)
    'dal',
    'dal_select2',
    # Django-filer allows for file and image management
    'easy_thumbnails',
    'filer',
    # Makes Django CMS prettier
    'djangocms_admin_style',
    # Admin goes here, below apps which modify/extend admin features
    'django.contrib.admin',
    # For rich text in Django CMS
    'ckeditor_filebrowser_filer',
    # This permits simple task scheduling
    'huey.contrib.djhuey',
    # This helps to make forms pretty
    'crispy_forms',
    # This allows for custom date range filtering of financials, etc.
    'daterange_filter',
    # This allows for PDF export of views
    'easy_pdf',
    # This allows for registration of project preferences
    'dynamic_preferences',
    # These are required for the CMS
    'sekizai',
    'cms',
    'menus',
    'treebeard',
    'djangocms_text_ckeditor',
    'djangocms_forms',
    # ## Typically, if you have a custom app for custom functionality,
    # ## it will be added here:
    # '< my_custom_app >',
    # ## This is the core app of the django-danceschool project that
    # ## is required for all installations:
    'danceschool.core',
    # ## These apps provide additional functionality and are optional,
    # ## but they are enabled by default:
    'danceschool.financial',
    'danceschool.private_events',
    'danceschool.discounts',
    'danceschool.vouchers',
    'danceschool.prerequisites',
    'danceschool.stats',
    'danceschool.news',
    'danceschool.faq',
    # ## Uncomment the lines below to add payment processor integration:
    # 'danceschool.payments.paypal',
    # 'danceschool.payments.stripe',
]

MIDDLEWARE = [
    # This middleware is required by Django CMS for intelligent reloading on updates.
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # These pieces of middleware are required by Django CMS
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
]

ROOT_URLCONF = 'school.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Ensures that the project's base templates directory is loaded.
        'DIRS': [os.path.join(BASE_DIR, 'school', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cms.context_processors.cms_settings',
                'sekizai.context_processors.sekizai',
            ],
        },
    },
]

WSGI_APPLICATION = 'school.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/static'