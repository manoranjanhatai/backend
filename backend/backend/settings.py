import os
from pathlib import Path
import secrets

print(secrets.token_urlsafe(50))
SECRET_KEY = 'GaosmCEBT0ML6ocHcBS7ozM0Xgku0Yc6SQjldF1E6FVWBYpBV0J6XEbUjHUt9uIocsY'



BASE_DIR = Path(__file__).resolve().parent.parent


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

INSTALLED_APPS = [
    "corsheaders",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes', 
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',  
    'users',  
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # ✅ आवश्यक आहे
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # ✅ आवश्यक आहे
    'django.contrib.messages.middleware.MessageMiddleware',  # ✅ आवश्यक आहे
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Allow React frontend
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "x-requested-with",
]


ALLOWED_HOSTS = ['localhost', '127.0.0.1']
ROOT_URLCONF = 'backend.urls'
DEBUG = True  


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangotest',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
AUTH_USER_MODEL = 'users.User'
