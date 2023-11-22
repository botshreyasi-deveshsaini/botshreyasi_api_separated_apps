"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&frid8c*42qh56c+@a013-pqr1q+$0#v)93fosy0#pwt-+fi=#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ALLOWED_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
AUTHENTICATION_BACKENDS = ('authorization.auth.Auth',)

# Application definition

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.sites',
    # 'RESUME_PARSERCHANNELS',
    # 'RESUME_PARSER',
    'tracker',
    'message_tempelate',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'authorization',
    'application',
    'userprofile',
    'rolepermission',
    'candidate',
    'smtpdetail',
    'history',
    'master',
    'departments',
    'bot',
    'jobs',
    'message_logs',
    'emailconfig',
    'candidate_status',
    'call',
    'referer',
    'my_refers',
    'campaign',
    'email_log',
    'message_log',
    'campaign_trigger',
    'chat',
    'url_shortner',
    'interview'

]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
    'api.middleware.AutoIPMiddleware',
]

AUTH_USER_MODEL = 'authorization.User'
CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = 'api.urls'
CORS_ORIGIN_WHITELIST = [
    'http://localhost:4200',
]
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'PATCH',
    'POST',
    'PUT',
    'OPTION'
]

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


WSGI_APPLICATION = 'api.wsgi.application'
ASGI_APPLICATION = 'api.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}
# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'bot',
#         'USER': 'botshreyasi',
#         'PASSWORD': 'Manoj@123!@#',
#         'HOST': 'botshreyasi.mysql.database.azure.com',
#         'PORT': '3306',
#     },
#     'mysqlslave': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'bot',
#         'USER': 'botshreyasi',
#         'PASSWORD': 'Manoj@123!@#',
#         'HOST': 'botshreyasi.mysql.database.azure.com',
#         'PORT': '3306',
#     }
# }


DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'bot',
    #     'USER': 'root',
    #     'PASSWORD': 'password',
    #     'HOST': 'localhost',
    #     'PORT': '3306',
    # },
    # 'mysqlslave': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'bot',
    #     'USER': 'root',
    #     'PASSWORD': 'password',
    #     'HOST': 'localhost',
    #     'PORT': '3306',
    # }

    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bot',
        'USER': 'dev_botshreyasi',
        'PASSWORD': 'Test@123!@#',
        'HOST': 'bot-shreyasi-test.mysql.database.azure.com',
        'PORT': '3306',
    },
    'mysqlslave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bot',
        'USER': 'dev_botshreyasi',
        'PASSWORD': 'Test@123!@#',
        'HOST': 'bot-shreyasi-test.mysql.database.azure.com',
        'PORT': '3306',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
    }
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'resume_data/')


"""================ CELERY SETTING ======================="""
# CELERY_BROKER_URL = 'http://0.0.0.0:8000/PROGRES/'

# CELERY_BROKER_URL = 'redis://h:p1f32b9a309b588283093e94d3a85d08e7263b9bb79572b25bd9ffcd6cec2f980@ec2-50-16-55-44.compute-1.amazonaws.com:23589'

# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_BACKEND = 'django-db'


CELERY_CACHE_BACKEND = 'django-cache'


Request_URL = "https://botshreyasi.com/"
SELF_DOMAIN = "http://127.0.0.1:8000/"
# EMAIL_DOMAIN = "botshreyasi.com"
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'email-smtp.ap-south-1.amazonaws.com'
# EMAIL_PORT = 587  # or the appropriate port for your region
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'AKIA55PGT2FTUK6FE6LR'
# EMAIL_HOST_PASSWORD = 'BNGREOM7nPpsk1yG6rS2yCG4+NieMbnYq+hYf03kWYJz'
EMAIL_DOMAIN = "botshreyasi.com"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465  # or the appropriate port for your region
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'devesh.s@botshreyasi.com'
EMAIL_HOST_PASSWORD = 'Alwar@123'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=180),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'django.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }