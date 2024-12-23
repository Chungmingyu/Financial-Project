# """
# Django settings for moneystark project.

# Generated by 'django-admin startproject' using Django 4.2.11.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.2/topics/settings/

# For the full list of settings and their values, see
# https://docs.djangoproject.com/en/4.2/ref/settings/
# """

# import environ
# import os
# from pathlib import Path

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent


# # API KEY 숨기기

# env = environ.Env(DEBUG=(bool, True))
# environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))
# DEPOSIT_API_KEY = env('DEPOSIT_API_KEY')
# EXCHANGE_API_KEY = env('EXCHANGE_API_KEY')
# MAP_API_KEY = env('MAP_API_KEY')


# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-=x-u1f(2kfjeb+d27=^c=t%l&!uqpli9eodg)q62td#&lb-fnk'

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# ALLOWED_HOSTS = []


# # Application definition

# INSTALLED_APPS = [
#     'boards',
#     'bankmap',
#     'accounts',
#     'exchanges',
#     'news',
#     'surveys',
#     'moneys',
#     'rest_framework',
#     'rest_framework.authtoken',
#     'dj_rest_auth',
#     'corsheaders',
#     'django.contrib.sites',
#     'allauth',
#     'allauth.account',
#     'allauth.socialaccount',
#     'dj_rest_auth.registration',
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
# ]

# SITE_ID = 1

# REST_FRAMEWORK = {
#     # Authentication
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.TokenAuthentication',
#     ],
#     # permission
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.AllowAny',
#     ],
# }

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     "corsheaders.middleware.CorsMiddleware",
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'allauth.account.middleware.AccountMiddleware',
# ]

# ROOT_URLCONF = 'moneystark.urls'

# # 개발 환경에서만 True로 설정 가능 (보안 위험)
# CORS_ALLOW_ALL_ORIGINS = True
# # CORS_ALLOWED_ORIGINS =
# # 특정 도메인만 허용
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:5173',  # Vue 개발 서버
#     'http://127.0.0.1:5173',  # 대체 로컬 개발 서버 (optional)
# ]


# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [
#             BASE_DIR / 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'moneystark.wsgi.application'


# # Database
# # https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# # Password validation
# # https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# # Internationalization
# # https://docs.djangoproject.com/en/4.2/topics/i18n/

# LANGUAGE_CODE = 'ko-kr'

# TIME_ZONE = 'Asia/Seoul'

# USE_I18N = True

# USE_TZ = True


# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = 'static/'

# # Default primary key field type
# # https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# AUTH_USER_MODEL = 'accounts.User'

# # 추가로 넣은 코드들
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.TokenAuthentication',
#         'rest_framework.authentication.BasicAuthentication',
#     ],
# }

# DEFAULTS = {
#     'REGISTER_SERIALIZER': 'dj_rest_auth.registration.serializers.RegisterSerializer',
# }

# # settings.py
# REST_AUTH = {
#     'REGISTER_SERIALIZER': 'accounts.serializers.CustomRegisterSerializer',
#     'USER_DETAILS_SERIALIZER': 'accounts.serializers.CustomUserDetailsSerializer',
# }


# # 집가서 추가로 넣은 코드
# # 이메일은 비어도 된다고 넣어놨음 일단은
# ACCOUNT_EMAIL_VERIFICATION = 'none'
# ACCOUNT_EMAIL_REQUIRED = False

# # REST-AUTH 회원가입 기본 Serailizer 재정의
# REST_AUTH = {
#     'REGISTER_SERIALIZER': 'accounts.serializers.CustomRegisterSerializer',
#     'USER_DETAILS_SERIALIZER': 'accounts.serializers.CustomUserDetailsSerializer',
# }

# ACCOUNT_ADAPTER = 'accounts.models.CustomAccountAdapter'

# # 241120 추가 코드
# # INSTALLED_APPS += ['corsheaders']
# # MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')
# # CORS_ALLOW_ALL_ORIGINS = True  # 개발용으로만 사용

import environ
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# API KEY 숨기기
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))
DEPOSIT_API_KEY = env('DEPOSIT_API_KEY')
EXCHANGE_API_KEY = env('EXCHANGE_API_KEY')
MAP_API_KEY = env('MAP_API_KEY')
GOOGLE_API_KEY = env('GOOGLE_API_KEY')
GOOGLE_CSE_ID = env('GOOGLE_CSE_ID')
FINNHUB_API_KEY = env('FINNHUB_API_KEY')
UPBIT_API_KEY = env('UPBIT_API_KEY')
UPBIT_SECRET_KEY = env('UPBIT_SECRET_KEY')
HOME_API_KEY = env('HOME_API_KEY')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=x-u1f(2kfjeb+d27=^c=t%l&!uqpli9eodg)q62td#&lb-fnk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'recommendations',
    'boards',
    'bankmap',
    'accounts',
    'exchanges',
    'news',
    'surveys',
    'moneys',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'corsheaders',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # 토큰 인증
        'rest_framework.authentication.BasicAuthentication',  # 기본 인증
        'rest_framework.authentication.SessionAuthentication',  # 세션 인증 추가
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'moneystark.urls'

# CSRF Trusted Origins에 프론트엔드 주소 추가
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',  # 프론트엔드 개발 환경 도메인
    'http://127.0.0.1:5173',  # 필요할 경우 추가
]
CORS_ALLOW_CREDENTIALS = True
# 개발 환경에서만 True로 설정 가능 (보안 위험)
CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS =
# 특정 도메인만 허용
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Vue 개발 서버
    'http://127.0.0.1:5173',  # 대체 로컬 개발 서버 (optional)
    "http://localhost:8000",
    'http://127.0.0.1:5173'
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'moneystark.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
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

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model 설정
AUTH_USER_MODEL = 'accounts.User'

# dj-rest-auth 기본 serializer 설정
REST_AUTH = {
    'REGISTER_SERIALIZER': 'accounts.serializers.CustomRegisterSerializer',
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.CustomUserDetailsSerializer',
}

# 이메일 관련 설정
ACCOUNT_EMAIL_VERIFICATION = 'none'  # 이메일 인증을 하지 않음
ACCOUNT_EMAIL_REQUIRED = False  # 이메일 필드 비필수로 설정

# 커스텀 어댑터 설정
ACCOUNT_ADAPTER = 'accounts.models.CustomAccountAdapter'

# CORS 설정
CORS_ALLOW_ALL_ORIGINS = True
