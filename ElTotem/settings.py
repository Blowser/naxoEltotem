# ElTotem/settings.py

import os
from pathlib import Path

# Rutas base
BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY y DEBUG vía variables de entorno (o fallback)
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-rbz-bj-ux1w9wpz7%#d-9r)ni-6709j&7is)+0hq*kyw=c0ls5')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Dominios permitidos
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,web-production-e97d.up.railway.app')\
    .split(',')

# Aplicaciones
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

# Middleware, con WhiteNoise justo después de SecurityMiddleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ElTotem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # si tienes carpetas de templates personalizadas, agrégalas aquí
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

WSGI_APPLICATION = 'ElTotem.wsgi.application'

# Base de datos MySQL (Railway)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.getenv('DB_HOST', 'containers.railway.app'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'NAME': os.getenv('DB_NAME', 'railway'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
    }
}


# Internacionalización
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
## STATICFILES_DIRS = [BASE_DIR / 'static']   # tu carpeta local con CSS/JS/IMÁGENES
STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)

# Validación de contraseñas, etc.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Otros ajustes
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
