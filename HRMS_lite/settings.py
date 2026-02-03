"""
Django settings for HRMS_lite project.
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/topics/settings/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-_1!f2@+ctv^1&w3g!4*@#y(oi+6py5o_t_jf@#u1=)c$^6_ao7')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.railway.app', '.up.railway.app']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'HRMS',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'HRMS_lite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'HRMS_lite.wsgi.application'

import os

# --- ENVIRONMENT & DATABASE DEBUG ---
IS_PROD = os.environ.get('RAILWAY_ENVIRONMENT')

if IS_PROD:
    print("\n" + "="*40)
    print("RUNNING IN PRODUCTION (RAILWAY)")
    print("="*40)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('MYSQL_DATABASE') or os.environ.get('MYSQLDATABASE'),
            'USER': os.environ.get('MYSQL_USER') or os.environ.get('MYSQLUSER'),
            'PASSWORD': os.environ.get('MYSQL_PASSWORD') or os.environ.get('MYSQLPASSWORD'),
            'HOST': os.environ.get('MYSQL_HOST') or os.environ.get('MYSQLHOST'),
            'PORT': os.environ.get('MYSQL_PORT') or os.environ.get('MYSQLPORT', '3306'),
        }
    }
else:
    # LOCAL: Use decouple to read .env
    DB_NAME = config('MYSQL_DATABASE', default=config('DB_NAME', default='HRMS_lite'))
    DB_USER = config('MYSQL_USER', default=config('DB_USER', default='root'))
    DB_PASS = config('MYSQL_PASSWORD', default=config('DB_PASSWORD', default=''))
    DB_HOST = config('MYSQL_HOST', default=config('DB_HOST', default='localhost'))
    DB_PORT = config('MYSQL_PORT', default=config('DB_PORT', default='3306'))
    
    print("\n" + "!"*40)
    print("DEBUG: LOCAL ENVIRONMENT DETECTED")
    print(f"DATABASE: {DB_NAME}")
    print(f"USER:     {DB_USER}")
    print(f"HOST:     {DB_HOST}")
    if not DB_PASS:
        print("PASSWORD: [EMPTY] <--- THIS IS LIKELY THE CAUSE OF YOUR ERROR!")
    else:
        print(f"PASSWORD: [FOUND] (Length: {len(DB_PASS)})")
    print("!"*40 + "\n")
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASS,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
        }
    }

# Common settings for all environments
DATABASES['default']['OPTIONS'] = {
    'charset': 'utf8mb4',
    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
}
DATABASES['default']['CONN_MAX_AGE'] = 600


# Common settings for all environments

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'HRMS' / 'static',
]

# WhiteNoise configuration for serving static files
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/6.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
