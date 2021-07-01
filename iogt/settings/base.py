"""
Django settings for iogt project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.utils.translation import gettext_lazy as _

import django.conf.locale

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'home',
    'search',
    'iogt_users',
    'comments',
    'iogt_content_migration',
    'questionnaires',
    'messaging',
    'django.contrib.humanize',
    'wagtail_localize',
    'wagtail_localize.locales',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.modeladmin',
    'wagtailmenus',
    'wagtailmedia',
    'wagtailmarkdown',
    'wagtail_transfer',
    'wagtail.contrib.settings',

    'django_comments_xtd',
    'django_comments',
    'modelcluster',
    'taggit',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'sass_processor',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'iogt_users.middlewares.RegistrationSurveyRedirectMiddleware',
    'external_links.middleware.RewriteExternalLinksMiddleware',
]

# Prevent Wagtail's built in menu from showing in Admin > Settings
WAGTAILMENUS_MAIN_MENUS_EDITABLE_IN_WAGTAILADMIN = False

ROOT_URLCONF = 'iogt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "wagtail.contrib.settings.context_processors.settings",
                'wagtailmenus.context_processors.wagtailmenus',
                'wagtail.contrib.settings.context_processors.settings',
                "home.processors.show_welcome_banner",
            ],
        },
    },
]

WSGI_APPLICATION = 'iogt.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Authentication
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

AUTH_USER_MODEL = 'iogt_users.User'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4
        }
    }
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, 'static')

# Allauth settings (https://django-allauth.readthedocs.io/en/latest/configuration.html)
# ACCOUNT_SIGNUP_FORM_CLASS = 'iogt_users.forms.AccountSignUpAdditionalFieldsForm'

# Control the forms that django-allauth uses
ACCOUNT_FORMS = {
    "login": "allauth.account.forms.LoginForm",
    "add_email": "allauth.account.forms.AddEmailForm",
    "change_password": "allauth.account.forms.ChangePasswordForm",
    "set_password": "allauth.account.forms.SetPasswordForm",
    "reset_password": "allauth.account.forms.ResetPasswordForm",
    "reset_password_from_key": "allauth.account.forms.ResetPasswordKeyForm",
    "disconnect": "allauth.socialaccount.forms.DisconnectForm",
    # Use our custom signup form
    "signup": "iogt_users.forms.AccountSignupForm",
}
# ACCOUNT_SIGNUP_FORM_CLASS = 'iogt_users.extra_forms.AccountSignUpAdditionalFieldsForm'

# Wagtail settings

WAGTAIL_SITE_NAME = "iogt"
ACCOUNT_ADAPTER = 'iogt_users.adapters.AccountAdapter'

WAGTAIL_USER_EDIT_FORM = 'iogt_users.forms.WagtailAdminUserEditForm'
WAGTAIL_USER_CREATION_FORM = 'iogt_users.forms.WagtailAdminUserCreateForm'
WAGTAIL_USER_CUSTOM_FIELDS = ['first_name', 'last_name', 'email', 'terms_accepted']

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://iogt.site'

# SITE ID
SITE_ID = 1

# Comments
COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_MAX_THREAD_LEVEL = 1

# Miscellaneous
LOGIN_REDIRECT_URL = "/users/profile/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = 'account_login'
WAGTAIL_FRONTEND_LOGIN_URL = LOGIN_URL

#  To help obfuscating comments before they are sent for confirmation.
COMMENTS_XTD_SALT = (b"Timendi causa est nescire. "
                     b"Aequam memento rebus in arduis servare mentem.")

# Source mail address used for notifications.
COMMENTS_XTD_FROM_EMAIL = "noreply@example.com"

# Contact mail address to show in messages.
COMMENTS_XTD_CONTACT_EMAIL = "helpdesk@example.com"

COMMENTS_XTD_CONFIRM_EMAIL = False

COMMENTS_XTD_FORM_CLASS = 'comments.forms.CommentForm'



COMMENTS_XTD_APP_MODEL_OPTIONS = {
    'default': {
        'allow_flagging': True,
        'allow_feedback': True,
        'show_feedback': True,
        'who_can_post': 'users'
    }
}

WAGTAIL_I18N_ENABLED = True

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ('ar', _('Arabic')),
    ('ch', _('Chichewa')),
    ('en', _('English')),
    ('fr', _('French')),
    ('km', _('Khmer')),
    ('rw', _('Kinyarwanda')),
    ('rn', 'Kirundi'),
    ('ku', _('Kurdish')),
    ('mg', _('Malagasy')),
    ('ne', _('Nepali')),
    ('nr', _('Ndebele')),
    ('pt', _('Portuguese')),
    ('qu', _('Quechua')),
    ('ru', _('Russian')),
    ('sho', _("Shona")),
    ('es', _('Spanish')),
    ('sw', _('Swahili')),
    ('tg', _('Tajik')),
    ('ti', _('Tigrinya')),
    ('ur', _('Urdu')),
    ('uz', _('Uzbek')),
    ('zu', _('Zulu'))
]

EXTRA_LANG_INFO = {
    'ch': {
        'bidi': False,
        'code': 'ch',
        'name': 'Chichewa',
        'name_local': 'Chichewa',
    },
    'ku': {
        'bidi': False,
        'code': 'ku',
        'name': 'Kurdish',
        'name_local': 'Kurdish'
    },
    'mg': {
        'bidi': False,
        'code': 'mg',
        'name': 'Malagasy',
        'name_local': 'Malagasy',
    },
    'nr': {
        'bidi': False,
        'code': 'nr',
        'name': 'Ndebele',
        'name_local': 'Ndebele',
    },
    'qu': {
        'bidi': False,
        'code': 'qu',
        'name': 'Quechua',
        'name_local': 'Quechua',
    },
    'rn': {
        'bidi': False,
        'code': 'rn',
        'name': 'Kirundi',
        'name_local': 'Ikirundi',
    },
    'rw': {
        'bidi': False,
        'code': 'rw',
        'name': 'Kinyarwanda',
        'name_local': 'Kinyarwanda',
    },
    'sho': {
        'bidi': False,
        'code': 'sho',
        'name': 'Shona',
        'name_local': 'Shona',
    },
    'ti': {
        'bidi': False,
        'code': 'ti',
        'name': 'Tigrinya',
        'name_local': 'Tigrinya',
    },
    'zu': {
        'bidi': False,
        'code': 'zu',
        'name': 'Zulu',
        'name_local': 'Zulu',
    },
}

django.conf.locale.LANG_INFO.update(EXTRA_LANG_INFO)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

WAGTAILTRANSFER_SOURCES = {
    'iogt_global': {
        'BASE_URL': 'http://iogt.org',
        'SECRET_KEY': 'fake_secret_key_2',
    },}

WAGTAILTRANSFER_SECRET_KEY = 'fake_secret_key'

WAGTAILMENUS_FLAT_MENU_ITEMS_RELATED_NAME = 'iogt_flat_menu_items'

from .profanity_settings import *
