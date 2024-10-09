import os
from datetime import timedelta
from pathlib import Path

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c1wi@zd_^fp@leii=!p_9%*z^huy-$9-px@9sxicg4(w11z3th'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'authapp',

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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}



AUTHORIZATION_DIR = os.path.join(Path(BASE_DIR).parent, "authorization")
JWT_PRIVATE_KEY_PATH = os.path.join(AUTHORIZATION_DIR, "jwt_key")
JWT_PUBLIC_KEY_PATH = os.path.join(AUTHORIZATION_DIR, "jwt_key.pub")

# Script for creating the Private/Public Key Pair
if (not os.path.exists(JWT_PRIVATE_KEY_PATH)) or (
    not os.path.exists(JWT_PUBLIC_KEY_PATH)
):
    if not os.path.exists(AUTHORIZATION_DIR):
        os.makedirs(AUTHORIZATION_DIR)
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=4096, backend=default_backend()
    )
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(JWT_PRIVATE_KEY_PATH, "w") as pk:
        pk.write(pem.decode())
    public_key = private_key.public_key()
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    with open(JWT_PUBLIC_KEY_PATH, "w") as pk:
        pk.write(pem_public.decode())
    print("PUBLIC/PRIVATE keys Generated!")

# JWT Access validity duration in days
ACCESS_TOKEN_VALID_DURATION = 5
# JWT Refresh token validity duration in weeks
REFRESH_TOKEN_VALID_DURATION = 2
# Visit this page to see all the registered JWT claims:
# https://tools.ietf.org/html/rfc7519#section-4.1
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        days=ACCESS_TOKEN_VALID_DURATION
    ),  # "exp" (Expiration Time) Claim
    "REFRESH_TOKEN_LIFETIME": timedelta(
        weeks=REFRESH_TOKEN_VALID_DURATION
    ),  # "exp" (Expiration Time) Claim
    "ROTATE_REFRESH_TOKENS": True,  # When set to True, if a refresh token is submitted to the TokenRefreshView, a new refresh token will be returned along with the new access token.
    "BLACKLIST_AFTER_ROTATION": False,  # If the blacklist
}
