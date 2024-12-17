import os
from datetime import timedelta
from logging.handlers import RotatingFileHandler
# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"BASE_DIR {BASE_DIR}")

# Secret Key (use a secure key in production)
SECRET_KEY = 'your-secret-key'  # Replace with a secure key

# Debug Mode
DEBUG = True  # Set to False in production

# Allowed Hosts
ALLOWED_HOSTS = ['*']  # Replace with your domain names or IP addresses

# PayPal Business Email and Mode

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django REST Framework
    'corsheaders',  # Django CORS Headers
    'paypal.standard',  # Django PayPal
    'myapp',
    
]

# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.gzip.GZipMiddleware',  # For compression
    # 'django.middleware.cache.CacheMiddleware',  # For caching
    # 'django.middleware.locale.LocaleMiddleware',  # For language support
    # 'django.middleware.transaction.TransactionMiddleware',  # For DB transactions
]

# URL Configuration
ROOT_URLCONF = 'myproj.urls'  # Replace with your project name

# WSGI Application
WSGI_APPLICATION = 'myproj.wsgi.application'  # Replace with your project name

# ASGI Application
ASGI_APPLICATION = 'myproj.asgi.application'  # Replace with your project name

# Database Configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Static Files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media Files (Uploaded files)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Templates Configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# Password Validation
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

# REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# JWT Settings (for `djangorestframework-simplejwt`)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=90),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}
# CORS Headers Configuration
CORS_ALLOW_ALL_ORIGINS = True

# Email Configuration (Use SMTP in production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = "meirevenhaim018@gmail.com"
EMAIL_HOST_PASSWORD = "bttoacfzzmlzkhxp"
EMAIL_PORT = 465  # SMTP port
EMAIL_USE_SSL = True  # Use SSL for secure connection


# PayPal Configuration
PAYPAL_MODE = 'sandbox'  # or 'live' for production
PAYPAL_CLIENT_ID = 'AcTg13p-nTvInt70-aj_Kj-d-2CcyWUflaoP8hhKRnWYYAOUOsmgQiGHbLack1Ln912UtnCBneKiZJ4y'
PAYPAL_CLIENT_SECRET = 'EEjItYIIZKwfF1c7d1VH9DAEdRzVCj0inPsa4l2DdoZt5J9DQ8n2J5huagsGt9lTzLHWf7JKOOC8HxW-'
PAYPAL_RECEIVER_EMAIL = 'meiro@meiro.com'
PAYPAL_TEST = True  # Set False when going live
# URLs for PayPal's return/cancel pages (use dummy URLs for now)
PAYPAL_NOTIFY_URL = 'http://localhost:8000/paypal-ipn/'
PAYPAL_RETURN_URL = 'http://localhost:8000/paypal-return/'
PAYPAL_CANCEL_URL = 'http://localhost:8000/paypal-cancel/'
DEFAULT_FROM_EMAIL = '<your-email@example.com>'
PAYPAL_API_BASE_URL = "https://api.sandbox.paypal.com"  # Sandbox environment


# Language and Time Zone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Default Auto Field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis_server:6379/1',  # Use the correct Redis DB (0 or 1, etc.)
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}



# Session setup (if you want to use Redis for sessions)
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'app.log'),
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'myapp': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

